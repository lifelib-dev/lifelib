# Pandas inputs in product models

Product Data Cells load input tables as ordinary pandas DataFrames and Series.
Formulas select values using pandas indexing, with explicit row keys and
column labels. Keep the original ordering of policy keys and use the model's
declared categories and parameter ranges.

The compiler can prepare eligible pandas reads for native execution. Other
reads use pandas semantics. The compilation audit identifies the selected
path for each reported read.
