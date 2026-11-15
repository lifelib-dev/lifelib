# Variable Universal Life (VUL)

[Product Specification](product-spec.md) defines the representative product and
[Technical Notes](technical-notes.md) derive its liability cash flow model.
[Implementation Notes](model.md) explain how `VUL_US_S` implements those notes and what was
standardized to do so; the cells reference generated from the model's own docstrings
follows it. How `VUL_US_SEC` extends `VUL_US_S` is explained in [In-Force Implementation
Notes](model-sec.md), and the cells reference of `VUL_US_SEC` follows it. Every source any
of them cites is in [Sources](sources.md).

```{toctree}
:maxdepth: 1

product-spec
technical-notes
model
VUL_US_S/VUL_US_S
model-sec
VUL_US_SEC/VUL_US_SEC
sources
```
