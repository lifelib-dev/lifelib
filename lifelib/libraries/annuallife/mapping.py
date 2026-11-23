"""Alias module for name_mapping.

Provides access to model_new -> TradLife_A name mappings.
"""
from lifelib.libraries.annuallife.name_mapping import (
    MODEL_NAME_MAPPING,
    SPACE_NAME_MAPPING,
    CELL_NAME_MAPPING,
    REF_NAME_MAPPING,
    PARAM_NAME_MAPPING,
    map_space,
    map_cell,
    map_ref,
    map_param,
    map_name,
    reverse_map_cell,
    get_space_mapping,
)

__all__ = [
    "MODEL_NAME_MAPPING",
    "SPACE_NAME_MAPPING",
    "CELL_NAME_MAPPING",
    "REF_NAME_MAPPING",
    "PARAM_NAME_MAPPING",
    "map_space",
    "map_cell",
    "map_ref",
    "map_param",
    "map_name",
    "reverse_map_cell",
    "get_space_mapping",
]
