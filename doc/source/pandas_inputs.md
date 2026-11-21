# Explicit pandas input preparation

Use the existing owned `Table` and `Record` structures for calculation inputs.
Public pandas Data Cells and reports retain their original types and contracts.

```python
from lifelib import pandas_inputs as inputs, typed_inputs as tables

# A preparation Cell depends on the unchanged public mortality-table Cell.
def prepared_mortality():
    return inputs.table(mort_table(), columns=('mort_rate',), groups=('sex',))

# An actuarial formula uses the same table helpers as adjusted MYGA/VA.
q = tables.lookup(tables.subtable(prepared_mortality(), sex()), age(t), 'mort_rate')
```

`inputs.table` explicitly copies scalar input values into the existing `Table`,
optionally nested in group `Record`s. It preserves row order and selected-column
order. It does not implicitly sort, fill missing values, aggregate duplicate keys
or convert every column to float. Numeric scalar widths become owned Python
scalars during preparation; native provider resources are prepared from these
normal inputs using the existing MYGA/VA mechanisms.

`inputs.record(series)` prepares the fields of an already-selected public row.
A model may retain a public `model_point()` Series and give a separate preparation
Cell a normal dependency on it. `inputs.records(frame)` prepares row Records
without the cross-column numeric coercion that pandas `iterrows` can perform.
These are construction operations, not a second table framework.

The existing Table contract requires unique keys and nonempty unique string
columns. Unsupported scalar types, duplicate keys and ambiguous group declarations
raise explicitly; they are not silently normalized. Public pandas inputs remain
unchanged. Adjustments requiring other pandas semantics need their own qualified
conversion, selection or compatibility path. Native coverage is tracked per
operation rather than inferred from a constructor succeeding.

Live modelx invalidates dependent preparation through normal whole-value
replacement and cleanup rules. Mutation inside a pandas object is not automatically
tracked. Exported Python and compiled packages retain the existing requirement
for explicit cleanup/re-preparation. Native resources remain disposable; public
inputs and published Cell caches round-trip normally.

The calculation target is the same native level as qualified adjusted MYGA/VA:
typed numeric buffers and Cython provider operations, with separately accounted
preparation/public-output boundaries and preserved compatibility behavior.
Module-namespace helper calls require generic native metadata/lowering support;
Python/live/export parity alone does not qualify their native calculation path.

Complete keys can stay together in an expression:

```python
def prepared_mortality():
    return inputs.table(mort_table(), columns=('mort_rate',))

q = float(tables.lookup(prepared_mortality(), (sex(), age(t)), 'mort_rate'))
```

This avoids selecting an earlier group before later key components have been
evaluated. Native contextual providers pack admitted components on the C stack;
they retain string/object references and preserve boolean keys. The native view
reuses the same Table, includes empty inputs, prepares exact builtin numeric
conversions, and defers conversion errors until the selected scalar is read.
Pandas NA/NaT remain their original immutable singletons rather than being
changed to NaN. Other callable/type/layout cases keep the compatibility path.

`tables.keys(table)` returns the same owned key tuple in input order. Its
registered native iteration producer exposes an owner-retaining int64 span;
unsupported bool/float/text/wide-integer key spans decline admission without
calling a replacement function. Generator consumers belong to the separate
generator lowering implementation and need combined evidence.

The Table lookup contract is not an arbitrary pandas index interpreter. Every
source adjustment needs a checked key/column-domain equivalence. In particular,
some pandas MultiIndex `.at` missing-key errors expose an encoded integer.
Use `inputs.table(frame, columns=..., indexing='at')` to retain the necessary
owned levels/offsets/boolean-label metadata. Its native error path preserves
that behavior for admitted full scalar keys, including retained empty levels.
It stores no live pandas Index in the Table. This does not qualify unrelated
index shapes or all models by itself.

The earlier separate NumericTable provider is retained in experimental Git/evidence
history as a donor. It is not a second canonical API.
