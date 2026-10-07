"""DC2412-20C — 24V -> 12V 20A (240W) step-down converter, potted die-cast aluminium.

Source: suremarineservice.com/Heat/Converters/DC2412-20C_2.html (specs, 248 g, single
product photo).  The page gives no dimensions; the envelope (74 x 74 x 32 mm) is
taken from the near-identical 244 g unit in the same housing family (B087WWTSC4)
and the photo proportions.  Leads (left to right, facing the grommet): yellow
OUT+, black OUT-, black IN-, red IN+.  Lead length estimated 250 mm, ~12 AWG.

Run headless:  freecad.cmd dc2412_20c_converter.py
Frame: fins along X, leads exit -Y, mounting tabs at +-X, underside at Z=0.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
from fcutil import part, save, dump_mesh, HERE
import alu_converter

OUT = os.path.join(HERE, "dc2412_20c_converter.FCStd")

doc = App.newDocument("DC2412_20C")
prt = part(doc, "DC2412_20C", None, "DC2412-20C 24V-12V 20A converter")
alu_converter.build(doc, prt, {
    "body_x": 60.0, "body_y": 74.0, "height": 32.0, "core_h": 13.0,
    "n_fins": 13, "fin_t": 2.2, "wall_t": 3.0, "n_low": 3, "low_h": 25.0,
    "posts": [(-18, 4), (12, 4), (-6, 8), (20, 9), (-20, 10), (4, 1)], "post_r": 3.2,
    "tab_len": 7.0, "tab_w0": 56.0, "tab_w1": 36.0, "tab_t": 4.0, "hole_d": 4.5, "hole_in": 3.8,
    "label_size": (48, 30),
    "label_lines": [("DC2412-20C", 5.0), ("IN 24V (20-30V)", 3.2), ("OUT 12V 20A 240W", 3.2)],
    "grommet": (36.0, 12.0, 5.0), "grommet_z": 2.0,
    "wires": [("yellow", 4.6), ("black", 4.6), ("black", 4.6), ("red", 4.6)],
    "wire_pitch": 7.5, "wire_len": 250.0,
})
save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "dc2412_20c_converter.json"))
