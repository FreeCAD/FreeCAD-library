"""Hokuyo UBG-04LX-F01 scanning laser rangefinder (URG-04LX family, automotive F01).

Approx. 50 x 50 x 70 mm.  Origin: centre of the mounting base underside, Z up,
scan window faces +Y (front).  Scan plane ~ z = 51.
Run: freecad.cmd hokuyo_ubg04lx_f01.py
"""
import os
import sys

sys.path.insert(0, "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
from fcutil import V, box, rbox_c, cyl, fuse, cut, compound, text, part, feat, save, dump_mesh, HERE

BLACK = (0.10, 0.10, 0.11)
GREY = (0.28, 0.29, 0.31)
WIN = (0.05, 0.05, 0.08, 0.25)
METAL = (0.7, 0.7, 0.72)
WHITE = (0.9, 0.9, 0.9)

doc = App.newDocument("Hokuyo_UBG04LX_F01")
p = part(doc, "UBG04LX", None, "Hokuyo UBG-04LX-F01")

# square lower housing with M3 holes in the base plate
body = rbox_c(0, 0, 0, 50, 50, 41, r=4, r_top=1.5, r_bot=0.8)
body = cut(body, [cyl(1.3, 6, (x, y, -1)) for x in (-20, 20) for y in (-20, 20)] +
           [cyl(1.6, 6, (0, -12, -1))])  # alignment hole
feat(doc, p, "Housing", body, GREY, "Housing")
feat(doc, p, "Label", rbox_c(0, 25.05, 12, 30, 0.3, 14, r=0), WHITE, "Label")


def front_text(s, size, z, y=25.0, h=0.3):
    """Text standing on the +Y face, readable from the front."""
    t = text(s, size, 0, 0, 0, h)
    t.rotate(V(0, 0, 0), V(1, 0, 0), 90)    # glyph-up -> +Z
    t.rotate(V(0, 0, 0), V(0, 0, 1), 180)   # read left-to-right from +Y
    t.translate(V(0, y, z))
    return t


feat(doc, p, "Logo", front_text("HOKUYO", 4.5, 30, 25.0), WHITE, "Logo")
feat(doc, p, "Model", front_text("UBG-04LX-F01", 2.6, 19, 25.3), BLACK, "Model text")

# scanning head: collar, optical window, top cap
feat(doc, p, "Collar", cyl(21.5, 2.5, (0, 0, 41)), BLACK, "Head collar")
feat(doc, p, "Window", cyl(20.0, 16.0, (0, 0, 43.5)), WIN, "Scan window")
feat(doc, p, "Optics", fuse([cyl(9, 16, (0, 0, 43.5)), box(-6, 0, 47, 12, 14, 8)]), BLACK,
     "Rotor / optics")
cap = cyl(21.5, 10.5, (0, 0, 59.5))
cap = cap.makeFillet(2.0, [e for e in cap.Edges if abs(e.Vertexes[0].Z - 70) < 1e-6])
feat(doc, p, "Cap", cap, BLACK, "Top cap")

# rear cable gland + cable
feat(doc, p, "Gland", cyl(4.5, 8, (0, -25, 9), (0, -1, 0)), BLACK, "Cable gland")
feat(doc, p, "Cable", cyl(2.6, 40, (0, -33, 9), (0, -1, 0)), (0.05, 0.05, 0.05), "Cable")

doc.recompute()
save(doc, os.path.join(HERE, "hokuyo_ubg04lx_f01.FCStd"))
dump_mesh(doc, os.path.join(HERE, "preview", "hokuyo_ubg04lx_f01.json"))
