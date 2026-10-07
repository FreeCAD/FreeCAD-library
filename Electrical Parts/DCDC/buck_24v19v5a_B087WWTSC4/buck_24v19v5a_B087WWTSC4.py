"""Vikye/GYVRM 24V -> 19V 5A waterproof buck converter (Amazon UK B087WWTSC4).

Source: Amazon listing — size 7.4 x 7.4 x 3.2 cm (incl. tabs), 244 g, IP67, die-cast
aluminium with silicone seal, 13 cm leads; photos show the finned top, black
potted underside with a "GYVRM K241905" label, trapezoid tabs on the fin ends
and the grommet on a flat side wall.  Leads (left to right, facing the grommet):
yellow OUT+, black OUT-, black IN-, red IN+.

Run headless:  freecad.cmd waterproof_buck_24v19v5a_B087WWTSC4.py
Frame: fins along X, leads exit -Y, mounting tabs at +-X, underside at Z=0.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
from fcutil import part, save, dump_mesh, HERE
import alu_converter

OUT = os.path.join(HERE, "waterproof_buck_24v19v5a_B087WWTSC4.FCStd")

doc = App.newDocument("Buck_24V19V5A")
prt = part(doc, "Buck_24V19V5A", None, "24V-19V 5A waterproof buck converter")
alu_converter.build(doc, prt, {
    "body_x": 60.0, "body_y": 74.0, "height": 32.0, "core_h": 12.0,
    "n_fins": 11, "fin_t": 2.4, "wall_t": 3.0, "n_low": 2, "low_h": 24.0,
    "posts": [(-18, 3), (14, 3), (-4, 6), (20, 7), (-20, 8)], "post_r": 3.2,
    "tab_len": 7.0, "tab_w0": 56.0, "tab_w1": 36.0, "tab_t": 4.0, "hole_d": 4.5, "hole_in": 3.8,
    "label_size": (50, 28),
    "label_lines": [("GYVRM K241905", 3.6), ("DC-DC CONVERTER", 2.8), ("IN 24V  OUT 19V 5A", 2.8)],
    "grommet": (30.0, 10.0, 5.0), "grommet_z": 2.5,
    "wires": [("yellow", 3.0), ("black", 3.0), ("black", 3.0), ("red", 3.0)],
    "wire_pitch": 6.0, "wire_len": 130.0,
})
save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "waterproof_buck_24v19v5a_B087WWTSC4.json"))
