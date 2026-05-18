"""
Generate a demo STEP file: simplified centrifugal pump station assembly.
Produces data/models/pump_station.step with 20 named components.
Uses STEPControl_Writer (no XCAF) + post-processing to inject part names.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "data", "models", "pump_station.step")

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeCylinder,
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeSphere,
)
from OCC.Core.gp import gp_Trsf, gp_Vec
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static
from OCC.Core.IFSelect import IFSelect_RetDone


def _translate(shape, dx=0.0, dy=0.0, dz=0.0):
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(dx, dy, dz))
    return BRepBuilderAPI_Transform(shape, trsf, True).Shape()


# (name, kind, *dims, dx, dy, dz)
PARTS = [
    ("Pump Housing P-101",              "cyl",    80, 120,      0,     0,     0),
    ("Suction Flange P-101",            "cyl",    50,  30,      0,     0,   -30),
    ("Discharge Flange P-101",          "cyl",    40,  30,      0,     0,   120),
    ("Impeller P-101",                  "cyl",    60,  40,      0,     0,    40),
    ("Drive Shaft P-101",               "cyl",    15, 200,      0,     0,   -80),
    ("Motor Housing M-101",             "box",   160, 120, 160,   -80,   -60,  -240),
    ("Cooling Fan M-101",               "cyl",    70,  20,      0,     0,  -260),
    ("Baseplate P-101",                 "box",   300, 200,  20,  -150,  -100,  -300),
    ("Inlet Pipe DN80",                 "cyl",    35,  90,      0,     0,  -120),
    ("Discharge Pipe DN65",             "cyl",    28, 120,      0,     0,   150),
    ("Gate Valve GV-101",               "box",    70,  70,  60,    -35,   -35,  -200),
    ("Check Valve CV-101",              "box",    60,  60,  50,    -30,   -30,   270),
    ("Pressure Gauge PI-101",           "sphere", 18,         100,     0,     0),
    ("Pressure Gauge PI-102",           "sphere", 18,         100,     0,   150),
    ("Flexible Coupling CK-101",        "cyl",    25,  20,      0,     0,  -100),
    ("Bearing Housing DE",              "cyl",    35,  25,      0,     0,   -50),
    ("Bearing Housing NDE",             "cyl",    30,  20,      0,     0,   100),
    ("Mechanical Seal P-101",           "cyl",    30,   8,      0,     0,    60),
    ("Vibration Sensor VS-101",         "box",    30,  20,  15,     90,     0,  -180),
    ("Temperature Sensor TE-101",       "box",    20,  15,  10,     40,    40,   -40),
]


def _make_shape(row):
    kind = row[1]
    if kind == "box":
        sx, sy, sz, dx, dy, dz = (float(v) for v in row[2:])
        return _translate(BRepPrimAPI_MakeBox(sx, sy, sz).Shape(), dx, dy, dz)
    if kind == "cyl":
        r, h, dx, dy, dz = (float(v) for v in row[2:])
        return _translate(BRepPrimAPI_MakeCylinder(r, h).Shape(), dx, dy, dz)
    if kind == "sphere":
        r, dx, dy, dz = (float(v) for v in row[2:])
        return _translate(BRepPrimAPI_MakeSphere(r).Shape(), dx, dy, dz)
    raise ValueError(f"Unknown kind: {kind}")


def _inject_names(filepath: str, names: list[str]) -> None:
    """Replace auto-generated PRODUCT names in STEP file with real part names."""
    with open(filepath, "r", encoding="ascii", errors="replace") as f:
        content = f.read()

    pattern = re.compile(
        r"(#\d+ = PRODUCT\()'Open CASCADE STEP translator [^']*?(\d+)',"
        r"\s*'Open CASCADE STEP translator [^']*?(\d+)'",
        re.DOTALL,
    )

    idx = 0

    def replacer(m):
        nonlocal idx
        if idx < len(names):
            safe = names[idx].replace("'", " ")
            idx += 1
            return f"{m.group(1)}'{safe}',\n  '{safe}'"
        return m.group(0)

    new_content = pattern.sub(replacer, content)

    with open(filepath, "w", encoding="ascii") as f:
        f.write(new_content)

    print(f"  Injected {idx} part names into STEP file")


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    print(f"Building {len(PARTS)}-part pump station…")
    writer = STEPControl_Writer()
    Interface_Static.SetCVal("write.step.schema", "AP214IS")

    for row in PARTS:
        shape = _make_shape(row)
        writer.Transfer(shape, STEPControl_AsIs)
        print(f"  + {row[0]}")

    status = writer.Write(OUT_PATH)
    if status != IFSelect_RetDone:
        print(f"ERROR: Write failed (status {status})")
        sys.exit(1)

    # Replace auto-generated OCC product names with real part names
    _inject_names(OUT_PATH, [row[0] for row in PARTS])

    size = os.path.getsize(OUT_PATH) // 1024
    print(f"Done → {OUT_PATH} ({size} KB)")


if __name__ == "__main__":
    main()
