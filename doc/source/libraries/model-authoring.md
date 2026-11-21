# Expressions for regional projection models

Use `modelx_helpers.pdn` for owned inputs and ordinary Python expressions for
financial calculations. Keep each CSV read in its Data Cell. A Projection Cell
can then select the values it needs through the same formulas in live modelx,
an exported Python model, and a compiled model.

| Expression | Domain and result | Native admission |
| --- | --- | --- |
| `pdn.table(frame, columns=..., groups=...)` | Own a DataFrame with unique leaf keys and unique string columns. Specify groups by index-level name. Group selection returns a Record or leaf Table. | The registered constructor can copy supported ungrouped frames with an integer or RangeIndex, compatible NumPy blocks or Python-backed string columns, and empty attrs. Grouped and column-pruned preparation use Python and pandas. Their prepared results can still support native reads. |
| `pdn.record(series)` and `pdn.index(labels)` | Own a row or ordered labels. Use `preserve_scalar_types=True` on a Record where the actual pandas or NumPy scalar type matters. | Preparation uses Python. A later field read or key traversal has its own admission conditions. |
| `pdn.lookup_float(table, key, column)` and `pdn.lookup_int(...)` | Convert a selected value from a complete scalar or tuple key and a named column. On a Record pass only the field and any keyword `default`. Use a default only when the financial rule defines the missing-key value. | The registered calls have declared `double` and signed 64-bit result types. The canonical provider can read an exact prepared owner with supported keys and columns. Native keyed reads admit exact strings, booleans, signed 64-bit integers, finite floats and tuples of these, with supported NumPy scalars. A stable Table view can also admit direct typed `table.lookup_float(...)` reads. |
| `pdn.lookup_bool`, `pdn.lookup_str`, `pdn.lookup_object` | Choose the result type required by the formula. The object form retains the original scalar type and missing values. | The canonical provider uses the same supported owner and key domains. The result ABI is boolean, string or object respectively. Use `-> object` on the enclosing and forwarding Cells when the public result must retain its exact scalar class. |
| `record[field]`, `table.slice(key)`, `pdn.row(table, key)`, `pdn.subtable(table, key)` | Read a field, a prepared row, or a group. Use `rows=True` for pandas-style row selection and keep tuple keys intact. | A resolvable Record Cell and literal string field can admit a native object field read. A registered row selection uses the canonical prepared Table, row metadata and an admitted key. A registered group selection uses an exact grouped Record. Chained object calls and unsupported key domains retain their ordinary compiled behavior. |
| `pdn.previous(table, key, column)` and `table.previous(key, column)` | Select the previous ordered key, including the requested key when present. | Integral keys on an exact Table with integral ordered keys can use the provider search. A typed Table source and suitable column binding can admit a numeric read. Keep authored lower and upper bounds explicit when the model applies them. |
| `pdn.keys`, `pdn.first_key`, `pdn.last_key`, `pdn.contains` | Traverse or test owned keys while preserving key order and multiplicity. | Ordered integer, finite-float and string spans can admit native traversal. Canonical `first_key`, `last_key` and `contains` can use the prepared Table's order or membership data. Object iteration is used for domains without an admitted span. |
| `range`, `sum`, `all`, `any`, `max`, `zip` | Preserve iteration order, filter conditions and a meaningful initial value such as `0.0`. | Ordinary expressions follow Cython's lowering. A registered reduction such as `pdn.sum_f64` can use a typed loop when the iteration bounds and yielded values are admitted and the compiler can preserve evaluation order and error behavior. |
| `pdn.column`, `pdn.group_sum`, `pdn.to_pandas` | Select a column, group report data or return pandas output. Use `report=True` to preserve report metadata and `first=` or `last=` for state columns in grouped reports. | Registered column selection can read an exact prepared Table. Grouped sums admit float64 report columns with a list or tuple of builtin signed 64-bit integer labels or a list or tuple of builtin float labels. Other layouts use pandas grouping. `to_pandas` materializes pandas output, including from lookup-only and grouped inputs. |

Treat category inputs as strings and convert them in the model with
`Category[label]`. Keep accepted aliases explicit, and let unknown labels fail
at the conversion Cell. Use named enum members in calculations that receive
already-converted categories.

Choose `pdn.lookup_float` for a read that must produce a float. Use the raw
lookup form when the actual scalar type matters.

## Give the compiler a representative sample

Use the same types, table layouts, key types and formula branches that the
production book uses. modelx Cells cache their results by default. Mark a
Cell as uncached in modelx if its formula needs to run on every call.
The compiler chooses the storage representation for a cached Cell.

Cached native signed-integer coordinates admit the range covered by
the sample, including observed negative indices. For a longer horizon, sample
it or declare the necessary upper extent using `cells_param_size` in the
Space's translation spec. For example, `{'cells_param_size': {'t': 361}}`
covers nonnegative `t` through 360. Include any needed negative indices in the
sample. A call outside the admitted range raises `IndexError`. A value that
cannot enter a signed 64-bit native slot exactly raises an error naming the
Cell or Reference. Widen the sample or spec when the model needs a wider type.

For the built-in Table provider, a Cell returning a Table needs a concrete
Table return annotation or a resolved forward of the same typed Cell to bind
its native view. The sample must also return the exact owner type consistently.
For example, the MYGA model uses this declaration on a Data Cell:

```python
def model_point_table() -> "modelx_helpers.immutable_inputs.Table":
    return pdn.table(pd.read_csv(input_dir() / model_point_file, index_col="point_id"), rows=True)
```

When a consumer reads a cached Table or grouped resource through a shared Data
Cell, export with `model.export(destination, locked_spaces=['Data'])` to admit
the reads that require a locked source Space. Use the name of the actual source
Space when it differs. Direct registered helper calls can still dispatch to a
provider for suitable arguments without that cached binding.

## Check the build report

In the compiled package, open `_mx_admission.json` and find the consumer Cell.
`native_helpers` lists linked provider operations, `native_numeric_helpers`
lists numeric specializations, and `native_reductions` counts admitted typed
loops. `return_type` shows the Cell's generated representation. `cache` shows
the storage choice. `dense_logical_domain` and `associative_logical_domain`
show the accepted integer ranges, with exclusive upper bounds. The optional
`dense_window` spec setting selects the physical dense region within an
admitted domain and leaves the Cell's authored cacheability unchanged.

The `reasons` field identifies Cells missed by the sample and names the source
when a matched read `requires Data in export locked_spaces`. For a sampled
provider result that requires a declaration, the report asks for a matching
return annotation or direct forwarding from a typed Cell. If a Table result
has an `object` return type, check its annotation, sample and forwarding
source. `original Cython representation` is the default reason when no
specific diagnostic applies. A linked helper may still dispatch through its
object path for a particular key or layout. Compare full policy outputs and
inspect the consumer's admissions when changing a performance-critical formula.

## Run another scenario

In live modelx, changing a Reference triggers dependency invalidation. For an
exported or compiled model, create a fresh model instance or process and install
changed inputs before requesting its first calculation. For example, with a
compatible MYGA input CSV containing policy 1:

```python
from pathlib import Path

from MYGA_US_S_nomx_cy import mx_model

base_cashflow = mx_model.Projection[1].net_cf(1)
scenario = type(mx_model)()
scenario.Data.model_point_file = str(Path("myga_stress_points.csv").resolve())
scenario_cashflow = scenario.Projection[1].net_cf(1)
```

Use the same sequence with the exported Python package. Install every changed
input on `scenario` before calling a reader, a projection Cell or `collect`.
