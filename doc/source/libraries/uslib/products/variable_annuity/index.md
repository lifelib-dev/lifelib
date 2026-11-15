# Variable Annuity with Living and Death Benefit Guarantees

[Product Specification](product-spec.md) defines the representative product and
[Technical Notes](technical-notes.md) derive its liability cash flow model.
[Implementation Notes](model.md) explain how `VA_US_S` implements those notes and what was
standardized to do so; the cells reference generated from the model's own docstrings
follows it. How `VA_US_SEC` extends `VA_US_S` is explained in [In-Force Implementation
Notes](model-sec.md), and the cells reference of `VA_US_SEC` follows it. Every source any of
them cites is in [Sources](sources.md).

```{toctree}
:maxdepth: 1

product-spec
technical-notes
model
VA_US_S/VA_US_S
model-sec
VA_US_SEC/VA_US_SEC
sources
```
