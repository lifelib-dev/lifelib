# The **Enums** Space

```{automodule} annuallife.TradLife_A.Enums
```

The {mod}`~annuallife.TradLife_A.Enums` space is a container for the
enum types used throughout {mod}`~annuallife.TradLife_A`. Each enum is
exposed as a child space:

* {mod}`annuallife.TradLife_A.Enums.ProductID` — product type codes
  (``TERM``, ``WL``, ``ENDW``).
* {mod}`annuallife.TradLife_A.Enums.SexID` — sex codes used to index
  mortality tables.
* {mod}`annuallife.TradLife_A.Enums.RateBasisID` — rate basis used by
  the commutation lookup (``PREM``, ``VAL``).

These enum spaces are referenced at the model level as ``ProductID``,
``SexID`` and ``RateBasisID`` and used by cells in
{mod}`~annuallife.TradLife_A.Projection` and its bases.
