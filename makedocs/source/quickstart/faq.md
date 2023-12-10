```{eval-rst}
:html_theme.sidebar_secondary.remove:
```
(faq)=
# FAQ and How-Tos

```{contents} 
:depth: 2
:local:
```

## lifelib FAQ and How-Tos

### I have a question about lifelib. Where should I ask the question?

If you have a question about lifelib, 
you can initiate a discussion [here](https://github.com/lifelib-dev/lifelib/discussions) on the lifelib development site on GitHub.
Open discussions are encouraged as they can be valuable resources for others who may have similar questions.

Alternatively, if you need to ask your question privately, 
you can email the development team at support@lifelib.io. 
However, note that public discussions are preferred for their communal benefit.

### I think I found a bug. Where do I report it?

If you may have found a bug in lifelib, 
you should report it by submitting an issue [here](https://github.com/lifelib-dev/lifelib/issues) on the development site of lifelib on GitHub.

Additionally, if you have a solution for the issue, 
you might want to consider contributing by creating a pull request (PR). 
This is a valuable way to participate in the development and improvement of lifelib.
For instructions on how to create a pull request, 
you can read the guidance provided 
by GitHub [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).


### What Python packages do I need to use lifelib?

When you install lifelib, it automatically installs modelx as a dependency if it
is not already installed in your environment. However, 
lifelib often requires additional Python packages for full functionality, 
notably pandas, numpy, and openpyxl. These packages are widely used and may already
be present in most Python environments; 
therefore, they are not automatically installed by lifelib. 
If these packages are not already installed in your environment, 
you should install them manually using either `pip` or `conda`.

Additionally, some specific libraries within lifelib may have their own unique package requirements. 
To identify any additional packages required by a particular library in lifelib, 
you should refer to the documentation page of that library.

To check whether a package is already installed in your environment, 
you can use the following commands in your command line or terminal,
replacing `package` with the name of the package you want to verify:

- For pip: `pip show package`
- For conda: `conda list package`

## modelx FAQ and How-Tos

This section provides FAQs and how-to guides specifically for lifelib models built with modelx.

### How do I run sample scripts in this section?

In the examples throughout this section, unless otherwise noted,
we use the `BasicTerm_S` model from the {mod}`basiclife` library as a reference.
This model, referred to as `model`, includes the `Projection` space.
It is assumed that you have already imported modelx, pandas,
and numpy with the aliases `mx`, `pd`, and `np`, respectively, in these examples.
Below is a sample code snippet that prepares the model and necessary variables 
for the examples in this section:

```pycon
>>> import pandas as pd

>>> import numpy as np

>>> import modelx as mx

>>> model = mx.read_model("BasicTerm_S")

>>> model.Projection
<UserSpace BasicTerm_S.Projection>
```

### How do I input data into a model?

To input data into a model, assign it to a name in a space. 
The code below assigns 0.03 to `r` in the `Projection` space in `model`.

```pycon
>>> model.Projection.r = 0.03

>>> model.Projection.r
0.03
```

Once `r` is defined in the `Projection` space, it can be referenced in formulas in the space. 
For example, the code below defines `pv_ann_due` in `Projection`, which is a Cells object whose formula references `r`.

```pycon
>>> @mx.defcells    # Define a Cells referencing r
... def pv_ann_due(n):
...     return ((1 - (1 + r) ** -n) / r) * (1 + r)

>>> pv_ann_due      # Confirm the Cells object is created
<Cells BasicTerm_S.Projection.pv_ann_due(n)>
```

This Cells object calculates the present value of an annuity due:

```pycon
>>> pv_ann_due(10)    # Calculate the present value of a 10-year annuity due with a 3% discount rate.
8.78610892187911

>>> model.Projection.r = 0.05   # Change the value of r

>>> pv_ann_due(10)    # Recalculate with a 5% discount rate. 
8.10782167564406
``` 

### What types of data can I input?

You can input any objects that support the *pickle* serialization protocol. 
This includes most built-in types like `int`, `float`, `str`, `list`, `tuple`, `dict`, `set`, etc. Additionally,
most types from standard libraries (e.g., `namedtuple`, `deque`, `ChainMap` from `collections`)
and popular third-party packages (e.g., `ndarray` from `numpy`, `DataFrame` and `Series` from `pandas`) are also supported.

### How is input data saved?

When a model is saved, objects input in a model are saved in the model. 
How the objects are saved depends on the types of the objects: 

- **Primitive Types (`bool`, `int`, `float`, `str`, `NoneType`):** These are saved as text literals in files corresponding to their parent spaces.
- **pandas DataFrame and Series:** If assigned by the assignment statement, 
  these are saved in a binary file named `data.pickle` within `_data` in the model directory.
  If assigned using the `new_pandas` method, they are saved in Excel or CSV files based on the specified parameters.
  See [this entry](how-to-save-as-excel-or-csv) for more details.
- **Other Objects:** These are serialized and stored collectively in `data.pickle`.

(how-to-save-as-excel-or-csv)=
### How do I save input data as Excel or CSV files?

To save pandas DataFrame and Series objects as Excel or CSV files, 
use the `new_pandas` method. 
This method allows for specifying the file format and additional parameters for saving. 
Here's an example showing how to assign a Series to `x` in the `Projection` space in `model` using `new_pandas`:

```pycon
>>> import pandas as pd

>>> data = pd.Series([0.03, 0.04, 0.05])

>>> data
0    0.03
1    0.04
2    0.05
dtype: float64

>>> model.Projection.new_pandas("x", "data.xlsx", data=data, file_type="excel")

```
See [modelx's document](https://docs.modelx.io/en/latest/tutorial/using_pandas.html) for more details.


### How do I input data into a model from an external file?

To input data into a model from an external input file, 
first, assign the file's path to a name in the model.
Then, create a Cells and define its formula to load data from the specified file path.
Here is an example:

```pycon

>>> model.Projection.data_path = r"C:\xxx\yyy\data.xlsx"

>>> @mx.defcells
... def data():
...     return pd.read_excel(data_path)
```

When `data` is called, it reads data from the file at the location specified as `data_path`
and returns it as a pandas DataFrame.
Note that this technique is not limited to the use in combination with pandas, 
but it can also be applied with any standard libraries or third-party tools, such as sqlite3, openpyxl, xarray, etc.
The key aspect is that the model only needs to store a string representing the file path, 
making this a flexible method for incorporating external data into your model.

### How do I import a Python module in a model?

To access a Python module from within the formulas of a modelx model, 
you need to assign the module to a name either in the model or in the specific space using the module. 
Assigning a module at the model level makes it accessible from any space within the model. 
If you assign it within a specific space, the module will only be accessible from that space.

Here's an example to illustrate this behavior.
In the code below, the scipy module is assigned to `sp` at the module level.
Then `pi` cells is defined in the `Projection` space, referring to the name `sp` in its formula:

```pycon
>>> import scipy

>>> model.sp = scipy    # Assign the scipy module to `sp` at the model level

>>> @mx.defcells
... def pi():
...     return sp.constants.pi   # Refer to the scipy module as sp 

>>> pi      # Confirm that `pi` is defined in `Projection`
<Cells BasicTerm_S.Projection.pi()>

>>> pi()    # Formula executes successfully
3.141592653589793
```
In the following example, the `scipy.constants` module is assigned to `sp_consts` in the `Projection` space. 
`pi` is then redefined to refer to `sp_consts`:

```pycon
>>> model.Projection.sp_consts = scipy.constants

>>> @mx.defcells
... def pi():
...     return sp_consts.pi     # Refer to the scipy.constants as sp_consts
        
>>> pi()
3.141592653589793

```

In the code below, another `pi()` is defined in `Space2`, 
and it fails because `sp_consts` is not defined in that space. 
This demonstrates the scope of module assignment
in modelx: modules assigned at the model level are globally accessible, 
while modules assigned within a specific space are only accessible within that space.

```pycon
>>> space2 = model.new_space("Space2")

>>> @mx.defcells
... def pi():
...     return sp_consts.pi
    
>>> pi      # `pi` is now also defined in `Space2`
<Cells BasicTerm_S.Space2.pi()>

>>> pi()
Traceback (most recent call last):
  ...
FormulaError: Error raised during formula execution
NameError: name 'sp_consts' is not defined

Formula traceback:
0: BasicTerm_S.Space2.pi(), line 2

Formula source:
def pi():
    return sp_consts.pi
```


### How do I speed up my model?

There are several approaches to increase the performance of a modelx model:

1. **Export to a Pure-Python Model:** 
   The simplest approach is to export your model as a pure-Python model. 
   Exported models do not depend on modelx and typically run faster and consume less memory. 
   This is because the exported models do not keep track of calculation dependencies.
   For details on how to export your model, 
   refer to [this entry](how-to-export-a-model).

2. **Optimization Through Profiling:**
   By profiling your model's execution, you can identify which formulas take the most time and optimize them accordingly. 
   This process involves analyzing the performance of various components of your model 
   and rewriting the more time-consuming formulas for efficiency.
   For guidance on profiling a model, see [this entry](how-to-profile-a-model).

3. **Vectorization:**
   Transforming your model into a vectorized model is another effective approach.
   In vectorized models, formulas are designed to apply the same logic to multiple model points simultaneously.
   For example, `BasicTerm_M` in the `basiclife` library is a vectorized version of `BasicTerm_S`,
   and `CashValue_ME` in the `savings` library is a vectorized version of `CashValue_SE`.
   These models use pandas Series objects or numpy arrays to handle values for multiple model points within a single formula. 
   By studying and understanding the logic of these vectorized models, 
   you can apply similar techniques to vectorize your model, potentially leading to significant performance improvements.


### How do I make my model consume less memory?

There are two main approaches to reduce memory consumption of your model:

1. **Export to a Pure-Python Model:** 
   Export your model to a pure-Python model using the `export` method. 
   Pure-Python models are generally more memory-efficient as they do not retain calculation dependency information. 
   In addition to memory efficiency, pure-Python models often execute faster than their original modelx counterparts. 
   However, note that this approach might have only a marginal effect in the case of vectorized models.
   For details on how to export your model, 
   refer to [this entry](how-to-export-a-model).

2. **Use `generate_actions` and `execute_actions` Functions in modelx:**
   Another effective yet more complex method involves 
   utilizing the `generate_actions` and `execute_actions` functions provided by modelx. 
   This process entails initially running the model with a small number of model points 
   to profile the sequence of formula execution.
   Then, you apply this profiling data to run the entire model points. 
   This is done by performing piecewise executions and value pasting, 
   effectively reducing memory usage during the computation process. 
   Refer to [this blog post](https://modelx.io/blog/2022/03/26/running-model-while-saving-memory/) on modelx's website for more details.

(how-to-profile-a-model)=
### How do I profile a formula execution?

To profile the execution of a formula in modelx, you can use the `trace_stack` context manager 
in combination with the `get_stacktrace` function. 
These tools allow you to track and analyze the performance of formula executions.

Below is an idiomatic example for profiling formula execution. 
You can use this code pattern directly, 
simply by replacing the specific formula execution line with the one you wish to profile.

```pycon
>>> with mx.trace_stack(maxlen=None):
...     BasicTerm_S.Projection[1].result_pv()   # Replace this line with your formula execution
...     stacktrace_data = mx.get_stacktrace(summarize=True)
...     df = pd.DataFrame.from_dict(stacktrace_data, orient="index")
UserWarning: call stack trace activated
UserWarning: call stack trace deactivated
```

When you run the code above, it activates the call stack trace, 
profiles the specified formula execution, and then deactivates the trace. 
The resulting profiling information is stored in a DataFrame, `df`. 
This DataFrame contains columns such as 'calls' and 'duration', 
which provide insights into the number of calls and the total time spent for each formula during the execution. 
This information is invaluable for understanding and optimizing the performance of your modelx formulas.

(how-to-export-a-model)=
### How do I export my model as a pure-Python model?

To export your model as a pure-Python model, use the `export` method.
The following code demonstrates how to export a model named `model` as `BasicTerm_S_nomx`:

```pycon
>>> model.export("BasicTerm_S_nomx")
```

Executing the above code will create a directory named `BasicTerm_S_nomx` in the current working directory. 
This directory is a Python package and operates independently of the modelx library. 
You can import and use this package just like any standard Python module. 
Inside this package, `mx_model` represents the pure-Python version of your model. 
It can be used in the same manner as the original model:

```pycon
>>> from BasicTerm_S_nomx import mx_model

>>> mx_model.Projection[1].pv_net_cf()
              Premiums       Claims    Expenses  Commissions  Net Cashflow
PV         8252.085856  5501.194898  755.366026  1084.604270    910.920661
% Premium     1.000000     0.666643    0.091536     0.131434      0.110387
```

### My model throws a FormulaError. How do I find the error?

When an exception occurs during the execution of formulas, a `FormulaError` is raised. 
The error message includes the type of the original error and 
a traceback detailing the sequence of formula executions leading to the error.

For example, consider a scenario where a `FormulaError` is encountered. 
In the `BasicTerm_S` model, the `pols_if_init` formula should return the number of policies in force at the start of the projection, 
which defaults to 1. Suppose you mistakenly modify the `pols_if_init` formula as follows:

```pycon
>>> mx_model.Projection.pols_if_init.formula = lambda : 1/0
```

Attempting to calculate `result_pv`, which depends on `pols_if_init`, will result in a `FormulaError`. 
The error message will look like this:

```pycon
>>> BasicTerm_S.Projection[1].result_pv()
Traceback (most recent call last):

    .. file trace ..

FormulaError: Error raised during formula execution
ZeroDivisionError: division by zero

Formula traceback:
0: BasicTerm_S.Projection[1].result_pv(), line 15
...
7: BasicTerm_S.Projection[1].pols_death(t=0), line 3
8: BasicTerm_S.Projection[1].pols_if(t=0), line 17
9: BasicTerm_S.Projection[1].pols_if_init(), line 1

Formula source:
lambda: 1/0
```

This message indicates the original error type (`ZeroDivisionError`), 
the formula execution traceback from the initially called formula to the one causing the error, 
and the source code of the problematic formula.

To obtain the complete traceback list, use the `get_traceback` function:

```pycon
>>> mx.get_traceback()
[(BasicTerm_S.Projection[1].result_pv(), 15),
 (BasicTerm_S.Projection[1].pv_premiums(), 9),
 (BasicTerm_S.Projection[1].premiums(t=0), 14),
 (BasicTerm_S.Projection[1].premium_pp(), 17),
 (BasicTerm_S.Projection[1].net_premium_pp(), 16),
 (BasicTerm_S.Projection[1].pv_claims(), 9),
 (BasicTerm_S.Projection[1].claims(t=0), 14),
 (BasicTerm_S.Projection[1].pols_death(t=0), 3),
 (BasicTerm_S.Projection[1].pols_if(t=0), 17),
 (BasicTerm_S.Projection[1].pols_if_init(), 1)]
```

Each tuple in the traceback list contains a formula and its corresponding line number. 
The line number indicates where each formula calls the next formula or, 
in the case of the last tuple, where the error was raised.

### How do I trace the dependency of formula execution?

In modelx, formula executions often depend on the results of other formula executions. 
To trace these dependencies, you can use the `precedents` method on the Cells.

For example, let's say you have executed the `result_pv` formula for `Projection[1]` as shown below:

```pycon
>>> model.Projection[1].result_pv()
              Premiums       Claims    Expenses  Commissions  Net Cashflow
PV         8252.085856  5501.194898  755.366026  1084.604270    910.920661
% Premium     1.000000     0.666643    0.091536     0.131434      0.110387
```

The formula definition of `result_pv` looks like this:

```pycon
>>> model.Projection[1].result_pv.formula
def result_pv():
    """Result table of present value of cashflows"""
    cols = ["Premiums", "Claims", "Expenses", "Commissions", "Net Cashflow"]
    pvs = [pv_premiums(), pv_claims(), pv_expenses(), pv_commissions(), pv_net_cf()]
    per_prem = [x / pv_premiums() for x in pvs]

    return pd.DataFrame.from_dict(
            data={"PV": pvs, "% Premium": per_prem},
            columns=cols,
            orient='index')
```

To list the formulas that `result_pv` depends on, 
call the `precedents` method on `result_pv`. 
Since `result_pv` does not have parameters, you can call it using `()`:

```pycon
>>> model.Projection[1].result_pv.precedents()
[BasicTerm_S.Projection[1].pv_premiums()=8252.085855522228,
 BasicTerm_S.Projection[1].pv_claims()=5501.194898364312,
 BasicTerm_S.Projection[1].pv_expenses()=755.3660261078039,
 BasicTerm_S.Projection[1].pv_commissions()=1084.6042701164513,
 BasicTerm_S.Projection[1].pv_net_cf()=910.92066093366,
 BasicTerm_S.Projection.pd=<module 'pandas' from 'C:\\Users\\...\\pandas\\__init__.py'>]
```

This will provide a list of formula executions that `result_pv()` depends on, 
along with their values. 
The `precedents` method returns a list of *Node* objects, 
each representing a formula execution along with its parameters and returned value.

You can further trace the dependencies of these formula executions. 
Note that here, `precedents` is a property, not a method, so parentheses are not needed:

```pycon
>>> model.Projection[1].result_pv.precedents()[0]
BasicTerm_S.Projection[1].pv_premiums()=8252.085855522228

>>> model.Projection[1].result_pv.precedents()[0].precedents
[BasicTerm_S.Projection[1].proj_len()=121,
 BasicTerm_S.Projection[1].premiums(t=0)=94.84,
 BasicTerm_S.Projection[1].premiums(t=1)=94.00577942943758,
 BasicTerm_S.Projection[1].premiums(t=2)=93.1788967327717,
 BasicTerm_S.Projection[1].premiums(t=3)=92.35928736545002,
 ...
 BasicTerm_S.Projection[1].premiums(t=119)=62.091142917461276,
 BasicTerm_S.Projection[1].premiums(t=120)=0.0,
 BasicTerm_S.Projection[1].disc_factors()=
 array([1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 0.99448063, 0.99402206, 0.9935637 ,
        0.99310556, 0.99264762, 0.9921899 , 0.99173238, 0.99127508,
        0.99081799, 0.99036111, 0.98990444, 0.98944798, 0.98645909,
        ...
        0.90887166, 0.90804496, 0.907219  , 0.90269051, 0.90183523,
        0.90098077, 0.90012712, 0.89927427, 0.89842223, 0.897571  ,
        0.89672058, 0.89587096, 0.89502215, 0.89417414, 0.89332693,
        0.88860731])]

>>> model.Projection[1].result_pv.precedents()[0].precedents[1].precedents
[BasicTerm_S.Projection[1].premium_pp()=94.84,
 BasicTerm_S.Projection[1].pols_if(t=0)=1]
```

It is also possible to trace formula executions in reverse order, i.e., 
find the formulas that depend on a particular formula execution (successors).
For example, to list formula executions that depend on `pols_if(0)`, 
use the `succs` method on `pols_if`. 
Each element in the returned list is a Node object, indicating the dependency:

```pycon
>>> model.Projection[1].pols_if(t=0)
Out[75]: 1

>>> model.Projection[1].pols_if.succs(t=0)
[BasicTerm_S.Projection[1].pols_death(t=0)=5.495304387248545e-05,
 BasicTerm_S.Projection[1].pols_if(t=1)=0.9912039163795611,
 BasicTerm_S.Projection[1].pols_lapse(t=0)=0.008741130576566412,
 BasicTerm_S.Projection[1].pv_pols_if()=87.01060581529134,
 BasicTerm_S.Projection[1].premiums(t=0)=94.84,
 BasicTerm_S.Projection[1].expenses(t=0)=305.0]

```

You can also retrieve successors further up by using the `succs` property on the Node objects:

```pycon
>>> model.Projection[1].pols_if.succs(t=0)[-2]
BasicTerm_S.Projection[1].premiums(t=0)=94.84

>>> model.Projection[1].pols_if.succs(t=0)[-2].succs
[BasicTerm_S.Projection[1].pv_premiums()=8252.085855522228,
 BasicTerm_S.Projection[1].commissions(t=0)=94.84]
```

If you use modelx from Spyder with modelx plug-in,
you can do the operations above using GUI in the MxAnalyzer widget.