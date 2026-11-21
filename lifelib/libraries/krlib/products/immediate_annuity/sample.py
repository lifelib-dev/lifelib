"""Sample run for mx2cy (modelx-cython): ships with the model, next to spec.py.

Run by `mx2cy exported --sample sample.py` in the folder holding the exported model package `exported` and the
model's CSV files. For every policy of the shipped book it projects the policy (collect_outputs) and then calls
every public zero-argument Cell of the item, its reports, so the trace covers the arguments only reports ask for.
A Cell that raises is recorded in sample_raised.json (Cell, exception, policies) and the run continues.
"""
import inspect
import json

from exported import mx_model

raised = {}
for key in map(int, mx_model.Data.model_point_table().index):
    item = mx_model.Projection[key]
    item.collect_outputs()
    for name, cell in sorted(item._cells.items()):
        if name.startswith("_") or inspect.signature(cell).parameters:
            continue
        try:
            cell()
        except Exception as error:  # noqa: BLE001 - recorded, not hidden
            entry = raised.setdefault(name, {"exception": f"{type(error).__name__}: {error}"[:300], "policies": []})
            entry["policies"].append(key)
with open("sample_raised.json", "w", encoding="utf-8") as stream:
    json.dump(raised, stream, indent=1)
