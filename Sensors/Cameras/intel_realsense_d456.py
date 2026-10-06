"""Intel RealSense D456 depth camera (IP65 variant of the D455).

Run headless:  freecad.cmd intel_realsense_d456.py  ->  intel_realsense_d456.FCStd
Envelope ~124 x 36 x 29.5 mm (W x D x H).  Axes: X = width, Y = depth (sensors face -Y),
Z = up.  Origin at the centre of the bottom face (on the 1/4"-20 tripod mount axis).
Sensor positions follow the D455 layout: 95 mm stereo baseline.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
import Part
from fcutil import V, box, rbox, cyl, fuse, cut, compound, text, part, feat, save, dump_mesh, HERE

OUT = os.path.join(HERE, "intel_realsense_d456.FCStd")

ALU = (0.50, 0.52, 0.55)
GLASS = (0.03, 0.03, 0.05)
LENS = (0.08, 0.10, 0.20)
RING = (0.20, 0.20, 0.22)
PROJ = (0.35, 0.10, 0.12)
BLACK = (0.08, 0.08, 0.09)
STEEL = (0.75, 0.75, 0.77)
WHITE = (0.92, 0.92, 0.92)

W, D, H = 124.0, 36.0, 29.5
RC = 9.0                    # front-view corner radius
Y0 = -D / 2                 # front face
ZC = H / 2


def xz_rrect(w, h, y0, depth, zc, r):
    """Prism with an XZ rounded-rectangle profile, extruded +Y from y0."""
    s = box(-w / 2, y0, zc - h / 2, w, depth, h)
    return s.makeFillet(r, [e for e in s.Edges if abs(e.tangentAt(e.FirstParameter).y) > 0.99])


def front_text(s, size, x, z, y, height=0.1):
    return text(s, size, x, y, z, height, rot=((x, y, z), (1, 0, 0), 90))


doc = App.newDocument("RealSense_D456")
cam = part(doc, "D456", None, "Intel RealSense D456")

# ---- aluminium housing with a front pocket for the cover glass
hous = xz_rrect(W, H, Y0, D, ZC, RC)
hous = hous.makeFillet(1.2, [e for e in hous.Edges
                             if all(abs(v.Y - Y0) < 1e-6 or abs(v.Y - (Y0 + D)) < 1e-6
                                    for v in e.Vertexes)])
GW, GH = W - 6.0, H - 6.0
hous = cut(hous, xz_rrect(GW, GH, Y0 - 1, 2.0, ZC, RC - 3))
# rear: USB-C screw-lock port, 2x M4 mounting holes; bottom: 1/4"-20 tripod mount
YR = Y0 + D
usb = xz_rrect(9.0, 3.4, YR - 8, 9, ZC, 1.6)
hous = cut(hous, [usb,
                  cyl(1.0, 6, (-9.0, YR - 5, ZC), (0, 1, 0)),
                  cyl(1.0, 6, (9.0, YR - 5, ZC), (0, 1, 0)),
                  cyl(2.0, 8, (-25.0, YR - 7, ZC), (0, 1, 0)),
                  cyl(2.0, 8, (25.0, YR - 7, ZC), (0, 1, 0)),
                  cyl(3.175, 8, (0, 0, -1))])
# shallow ribs on the top for grip / heat spreading
hous = cut(hous, [box(-40 + i * 10 - 0.6, Y0 + 8, H - 0.5, 1.2, D - 16, 1) for i in range(9)])
feat(doc, cam, "Housing", hous, ALU, "Aluminium housing (IP65)")

feat(doc, cam, "CoverGlass", xz_rrect(GW - 0.3, GH - 0.3, Y0 + 0.2, 0.8, ZC, RC - 3.1), GLASS,
     "Front cover glass")

# ---- sensors seen through the glass (sit 0.05 mm proud so they render)
YS = Y0 + 0.15
rings, lenses = [], []
for x, r in ((-47.5, 4.2), (47.5, 4.2), (30.0, 3.4)):   # left IR, right IR, RGB
    rings.append(cut(cyl(r + 1.4, 0.1, (x, YS, ZC), (0, 1, 0)), cyl(r, 1, (x, YS - 0.5, ZC), (0, 1, 0))))
    lenses.append(cyl(r, 0.1, (x, YS, ZC), (0, 1, 0)))
feat(doc, cam, "LensRings", compound(rings), RING, "Imager lens rings")
feat(doc, cam, "Lenses", compound(lenses), LENS, "Left/right IR imagers + RGB lens")
feat(doc, cam, "Projector", fuse([xz_rrect(9.0, 7.0, YS, 0.1, ZC, 1.5)]), PROJ, "IR dot projector")
feat(doc, cam, "IRLed", cyl(1.0, 0.1, (12.0, YS, ZC + 6.0), (0, 1, 0)), PROJ, "Status LED")
feat(doc, cam, "FrontText", compound([
    front_text("intel", 3.2, -27.0, ZC - 6.5, YS),
    front_text("RealSense", 2.4, -27.0, ZC + 6.8, YS)]), WHITE, "Front lettering")

# ---- port + mount inserts
feat(doc, cam, "USBC", cut(xz_rrect(8.4, 2.6, YR - 7.5, 7.0, ZC, 1.2),
                          xz_rrect(6.6, 1.4, YR - 7, 8, ZC, 0.6)), STEEL, "USB-C (screw-lock)")
feat(doc, cam, "USBTongue", box(-2.8, YR - 7, ZC - 0.35, 5.6, 6.0, 0.7), BLACK, "USB-C tongue")
inserts = [cut(cyl(2.0, 6, (x, YR - 6.5, ZC), (0, 1, 0)), cyl(1.65, 8, (x, YR - 7, ZC), (0, 1, 0)))
           for x in (-25.0, 25.0)]
inserts.append(cut(cyl(3.175, 6.5, (0, 0, -0.01)), cyl(2.7, 8, (0, 0, -1))))
inserts += [cut(cyl(1.0, 4, (x, YR - 4, ZC), (0, 1, 0)), cyl(0.8, 6, (x, YR - 5, ZC), (0, 1, 0)))
            for x in (-9.0, 9.0)]
feat(doc, cam, "Inserts", compound(inserts), STEEL, "M4 x2 rear, 1/4\"-20 bottom, M2 screw-lock")
rear_lbl = text("D456", 4, 0, YR, ZC + 8, 0.1, rot=((0, YR, ZC + 8), (1, 0, 0), -90))
rear_lbl.rotate(V(0, YR, ZC + 8), V(0, 1, 0), 180)  # read correctly from behind
feat(doc, cam, "RearLabel", rear_lbl, WHITE, "Rear label")

save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "intel_realsense_d456.json"), tol=0.1)
