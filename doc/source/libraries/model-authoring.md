# Authoring product models for native compilation

Keep policy and assumption inputs as pandas DataFrames or Series.
Use ordinary Python expressions in Cells and put policy-independent input
loads in Data Cells. Project and report using the same formulas in live
modelx and in a compiled model.

Use explicit pandas operations to select input values. For example,
`mort_table().loc[(sex(), age(t)), "mort_rate"]` selects a rate by row key and
column label. Define enum members for categories used in formulas and keep
the shipped labels in CSV inputs. Use `model_point_table().index` to iterate
over policy keys in their original order.

A product's `sample.py` exercises its compiled formulas. The matching
`spec.py` declares supported ranges for integer parameters such as projection
month and age. The product specifications describe the financial meaning of
these ranges and input domains.
