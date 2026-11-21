# Released US model fixtures

These twelve saved `_US_S` model directories are copied verbatim from the
lifelib 0.17.3 release, commit `d44068e2`. They contain no input tables or model
outputs. The SEC tests use these formulas and the CSVs shipped with each
product, so their existing cell-by-cell assertions continue to use the
released model's public cells, labels and intermediate values.

The model conventions and product tests continue to exercise the shipped
conversions. The conventions suite also compares the converted and released
cash flows on the SEC twin policies.
