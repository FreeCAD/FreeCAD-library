"""Heavy-duty 200 A 12 V relay (Ripca / Ripaults 2136/200 12V, as sold by EasyCabin
https://parts.easycabin.co.uk/products/relay-200a-12volt-heavy-duty).

Run headless:  freecad.cmd relay_200a_12v.py   ->  relay_200a_12v.FCStd

Black moulded block that mounts flat (back face down) by a single screw tab;
two M6 brass main studs (30 / 87) leave one edge, with the 85 / 86 coil blade
terminals between them.  Body size estimated from the listing photo
(~50 x 46 x 38 mm); no datasheet was available.

Axes: X = across the face, Y = towards the mounting tab (studs point -Y),
Z = up from the mounting surface (printed face on top).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
import Part
from fcutil import (V, box, rbox, rbox_c, cyl, fuse, cut, compound, text, part, feat, save,
                    dump_mesh, HERE)

OUT = os.path.join(HERE, "relay_200a_12v.FCStd")

BLACK = (0.07, 0.07, 0.08)
BRASS = (0.80, 0.62, 0.25)
STEEL = (0.75, 0.76, 0.78)
WHITE = (0.93, 0.93, 0.93)
TIN = (0.80, 0.80, 0.82)

W, L, D = 50.0, 46.0, 38.0       # body: X width, Y length, Z height
STUD_X = 13.0                    # studs at x = +-STUD_X
STUD_Z = 14.0                    # stud axis height above the mounting surface
STUD_LEN = 20.0                  # exposed M6 thread

doc = App.newDocument("Relay_200A_12V")
relay = part(doc, "Relay", None, "Relay 200A 12V (2136/200)")

# ---- body: rounded block with a slight draft on the top edges
body = rbox_c(0, 0, 0, W, L, D, r=5.0, r_top=2.0, r_bot=0.8)
# shallow boss on the stud face
body = fuse([body, rbox_c(0, -L / 2 - 1.0, 4, W - 8, 2.5, 22, r=1.5)])
feat(doc, relay, "Body", body, BLACK, "Body")

# mounting tab on the base plane, beyond the +Y edge
tab = fuse([rbox_c(0, L / 2 + 3, 0, 18, 12, 4, r=2),
            cyl(9, 4, (0, L / 2 + 9, 0))])
tab = cut(tab, cyl(3.1, 10, (0, L / 2 + 9, -1)))
tab = fuse([tab, rbox_c(0, L / 2 - 0.5, 0, 26, 3, 10, r=1)])  # gusset into the body
feat(doc, relay, "MountTab", tab, BLACK, "Mounting tab")

# ---- main studs (30, 87): hex collar, M6 thread, washer + nut
studs, nuts = [], []
for sx in (-STUD_X, STUD_X):
    y0 = -L / 2 - 1.0
    hexc = cyl(5.5, 3, (sx, y0, STUD_Z), (0, -1, 0))
    thread = cyl(3.0, STUD_LEN, (sx, y0 - 3, STUD_Z), (0, -1, 0))
    rings = [cyl(3.25, 0.5, (sx, y0 - 3.5 - i * 1.0, STUD_Z), (0, -1, 0))
             for i in range(int(STUD_LEN) - 1)]
    studs.append(fuse([hexc, thread] + rings))
    washer = cut(cyl(6.2, 1.2, (sx, y0 - 3, STUD_Z), (0, -1, 0)),
                 cyl(3.2, 3, (sx, y0 - 2, STUD_Z), (0, -1, 0)))
    hexnut = Part.makePolygon([V(sx + 5.77 * math.cos(a * math.pi / 3), y0 - 4.2,
                                 STUD_Z + 5.77 * math.sin(a * math.pi / 3)) for a in range(7)])
    hexnut = Part.Face(hexnut).extrude(V(0, -5, 0))
    hexnut = cut(hexnut, cyl(3.1, 8, (sx, y0 - 3, STUD_Z), (0, -1, 0)))
    nuts += [washer, hexnut]
feat(doc, relay, "Studs", compound(studs), BRASS, "Main studs M6 (30 / 87)")
feat(doc, relay, "Nuts", compound(nuts), STEEL, "Washers + nuts")

# ---- coil terminals (85, 86): 6.3 mm blades between the studs
blades = []
for bx in (-4.0, 4.0):
    b = box(bx - 0.4, -L / 2 - 1.0 - 9.0, 18.0 - 3.15, 0.8, 9.5, 6.3)
    b = cut(b, cyl(0.8, 2, (bx - 1, -L / 2 - 7.5, 18.0), (1, 0, 0)))
    blades.append(b)
feat(doc, relay, "CoilBlades", compound(blades), TIN, "Coil terminals 85 / 86")
feat(doc, relay, "BladeShroud", compound([rbox_c(0, -L / 2 - 1.8, 12.5, 16, 2.0, 11, r=1)]),
     BLACK, "Blade shroud")

# ---- printed face (top)
Z = D
pr = [
    text("RIPCA", 4.2, -10.0, 15.5, Z, 0.15),
    text("Ripaults", 3.0, 7.5, 15.5, Z, 0.15),
    text("2136/200 12V", 4.2, 0, 7.0, Z, 0.15),
    text("30 85", 3.2, -12, -15.5, Z, 0.15),
    text("86 87", 3.2, 12, -15.5, Z, 0.15),
]
# logo frame
frame = cut(rbox_c(-1, 15.5, Z, 36, 8, 0.15, r=1.5), rbox_c(-1, 15.5, Z - 1, 34.8, 6.8, 2, r=1))
pr.append(frame)
# schematic: contacts, coil, leads to the terminal numbers
lw = 0.35
for x0, y0, l, w in ((-14, -11, lw, 13), (14, -11, lw, 13), (-14, 2, 10, lw), (4, 2, 10, lw),
                     (-6, -11, lw, 8), (6, -11, lw, 8), (-6, -3, 4, lw), (2, -3, 4, lw)):
    pr.append(box(x0, y0, Z, l, w, 0.15))
pr.append(cut(box(-2, -5, Z, 4, 7, 0.15), box(-1.65, -4.65, Z - 1, 3.3, 6.3, 2)))  # coil
pr.append(box(-1.8, -4.6, Z, 3.6, 0.3, 0.15).rotated(V(0, -1.5, Z), V(0, 0, 1), 55))
contact = box(-4, 2, Z, 8, lw, 0.15)
contact.rotate(V(-4, 2, Z), V(0, 0, 1), 18)
pr += [contact] + [cyl(0.7, 0.15, (x, -12, Z)) for x in (-14, -6, 6, 14)]
feat(doc, relay, "Print", compound(pr), WHITE, "Printed face")

doc.recompute()
save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "relay_200a_12v.json"))
