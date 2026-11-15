# Fixed Indexed Annuity (FIA) with Guaranteed Lifetime Withdrawal Benefit

[Product Specification](product-spec.md) defines the representative product and
[Technical Notes](technical-notes.md) derive its liability cash flow model.
[Implementation Notes](model.md) explain how `FIA_US_S` implements those notes and what was
standardized to do so; the cells reference generated from the model's own docstrings
follows it. How `FIA_US_SEC` extends `FIA_US_S` is explained in [In-Force Implementation
Notes](model-sec.md), and the cells reference of `FIA_US_SEC` follows it. Every source any
of them cites is in [Sources](sources.md).

```{toctree}
:maxdepth: 1

product-spec
technical-notes
model
FIA_US_S/FIA_US_S
model-sec
FIA_US_SEC/FIA_US_SEC
sources
```
