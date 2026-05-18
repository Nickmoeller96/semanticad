"""STEP file loading via XCAF — returns flat list of named, positioned components."""

import os
from dataclasses import dataclass

from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Extend.DataExchange import read_step_file_with_names_colors


@dataclass
class PartEntry:
    name: str
    shape: object        # TopoDS_Shape (transform already applied)
    color: Quantity_Color


def load_step(filepath: str) -> list[PartEntry]:
    """Load a STEP file and return one PartEntry per component."""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(filepath)

    shape_dict = read_step_file_with_names_colors(filepath)

    parts: list[PartEntry] = []
    seen: set[int] = set()

    for shape, info in shape_dict.items():
        shape_id = id(shape)
        if shape_id in seen:
            continue
        seen.add(shape_id)

        raw_name = info[0] if info[0] else ""
        name = raw_name.strip() or "Part"
        color: Quantity_Color = info[1] if len(info) > 1 else Quantity_Color(
            0.7, 0.7, 0.7, Quantity_TOC_RGB
        )
        parts.append(PartEntry(name=name, shape=shape, color=color))

    return parts
