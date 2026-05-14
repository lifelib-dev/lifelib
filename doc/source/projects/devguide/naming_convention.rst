
.. _naming_convention:

Naming Convention
=================

.. note::

   This naming convention applies only to the projects introduced
   before lifelib 0.1.1. Libraries introduced 0.1.1 onwards
   do not follow this convention.

Python has a relatively strict coding style guide as
prescribed in the famous `PEP8`_ document.

.. _PEP8: https://www.python.org/dev/peps/pep-0008/

Since lifelib models are written in Python,
it is tempting to apply the naming convention in `PEP8`_ to lifelib as well.
However, in actuarial models, variable names, especially
cells names tend to be longer.
For example, it is impractical to type a cell name like this::

    directly_attributable_acquisition_expense_per_sumassured

In addition, lifelib spaces contain much more cells with similar names
than ordinary Python modules would contain variables.

To address these issues,
the naming convention original to lifelib is set up as prescribed below.

**Naming style**

For space and cells names, ``UpperCamelCase`` should be used.
However, when an abbreviation ending with
an upper case letter needs to be concatenated, ``_`` may be placed
after the letter to improve readability, such as ``PV_Cashflow``

**Concatenation order**

When the name of a cells is made up of two or more words,
the words(or their abbreviations) should be concatenated
in the natural order, i.e. modifiers followed by their modificand,
such as ``NetInsurCF`` and ``AccDeath``.
However, when a modifier indicates that the cells is a sub item
of the cells without the modifier,
the oder should be reversed, i.e.
the modificand comes first followed by its modifier, such as
``BenefitMat``, ``BenefitDeath``, ``BenefitSurr``.


**Abbreviation list**

Below is the list of abbreviations for words that are commonly used
as names of cells and spaces in lifelib projects.

.. table::

    ================== =========================
    Word               Abbreviation
    ================== =========================
    Accidental         Acc
    Accreted           Accr
    Acquisition        Acq
    Actual             Act
    Adjustment         Adj
    After              Aft
    Amortization       Amort
    Annual(ized)       Ann
    Annuity            Ann
    Asset              Ast
    Assumption         Asmp
    Attained           Att
    Before             Bfr
    Begin(ning)        Beg
    Cashflow           CF
    Catastrophe        Cat
    Change             Chg
    Charge             Chrg
    Commission         Comm
    Commutation        Comm
    Consumption        Cnsmp
    Correlation        Corr
    Coverage           Cov
    Death              Dth
    Decrease           Decr
    Disability         Disab
    Discount           Disc
    Dividend           Div
    Economic           Econ
    Estimated          Est
    Expected           Expct
    Expense            Exps
    Factor             Fac
    Finance            Fin
    Financial          Fin
    Frequency          Freq
    Fulfilment         Fluf
    Generation         Gen
    Hospitalization    Hosp
    Income             Incm
    Increase           Incr
    Incurred           Incur
    Inflation          Infl
    In-force           IF
    Initial            Init
    Insurance          Insur
    Interest           Int
    Investment         Invst
    Issue              Iss
    Loading            Load
    Longevity          Longev
    Maintenance        Maint
    Maturity           Mat
    Morbidity          Morbid
    Mortality          Mort
    Multiplier         Mult
    Policy             Pol
    Policies           Pols
    Premium            Prem
    Present Value      PV
    Product            Prod
    Projection         Proj
    Release            Rels
    Reserve            Rsrv
    Return             Ret
    Revision           Rev
    Scenario           Scen
    Sickness           Sick
    Sum Assured        SA
    Surgery            Surg
    Surrender          Surr
    Table              Tbl
    Transfer           Trans
    Unearned           Uern
    ================== =========================
