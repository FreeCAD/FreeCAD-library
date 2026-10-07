# Parametric FreeCAD models: sliding T-nuts M2, M3, M4 and M5 for 2020 aluminium extrusion (slot 6)
# Licence: CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/)
# Independently drawn generic part. Common supplier dimensions: 10 L x 9 W x 4.5 H, neck 6 W x 1.5 H.
# Chamfer size estimated to clear the sloped cavity of a 2020 slot-6 profile.
# Threads: modelled ISO 68-1 basic profile, coarse pitch, right-hand (internal thread, no tolerance class offset).
# Run: freecad.cmd make_tnuts_2020.py   (or paste into the FreeCAD Python console)
import FreeCAD as App, Part
from FreeCAD import Vector as V
import math, os

# ---- parameters (mm) ----
L = 10.0                     # length along the slot
BODY_W, BODY_H = 9.0, 3.0    # wide part that sits inside the slot cavity
NECK_W, NECK_H = 6.0, 1.5    # step that sits in the 6.2 mm slot opening (total height 4.5)
CHAMFER = 1.2                # 45 deg chamfer on lower body edges
SIZES = {"M2": 0.4, "M3": 0.5, "M4": 0.7, "M5": 0.8}   # nominal diameter -> coarse pitch
THREAD_CHAMFER = 0.4
OUT = os.environ.get("TNUT_OUT", os.getcwd())

# Origin: centre of the neck top face (bearing face against the mounted part's side of the slot).
# Z points out of the slot; the nut body extends to -Z. X = along the slot.
def thread_groove(d, pitch, z0, length):
    """Helical solids (one per turn) occupying the mating bolt's thread space, ISO 68-1 basic profile.
    Built a turn at a time: OCC booleans fail on a single swept face wrapping many turns."""
    H = math.sqrt(3) / 2 * pitch
    r_min, r_maj = (d - 1.25 * H) / 2, d / 2          # D1 = D - 1.0825 P, D
    over = 0.15                                        # extend inside the bore so the cut is clean
    w_min, w_root = 0.75 * pitch, 0.125 * pitch        # groove width at D1 and at D (flat root, P/8)
    slope = (w_min - w_root) / 2 / (r_maj - r_min)
    w_in = w_min + 2 * slope * over
    prof = Part.makePolygon([V(r_min - over, 0, z0 - w_in/2), V(r_maj, 0, z0 - w_root/2),
                             V(r_maj, 0, z0 + w_root/2), V(r_min - over, 0, z0 + w_in/2), V(r_min - over, 0, z0 - w_in/2)])
    helix = Part.makeHelix(pitch, pitch, r_min - over)
    helix.translate(V(0, 0, z0))
    ps = Part.BRepOffsetAPI.MakePipeShell(Part.Wire(helix))
    ps.setBiNormalMode(V(0, 0, 1))                     # keep the profile in an axial plane
    ps.add(prof)
    ps.build()
    ps.makeSolid()
    turn = ps.shape()
    turns = [turn.translated(V(0, 0, i * pitch)) for i in range(math.ceil(length / pitch))]
    return turns, r_min

def make_tnut(d):
    pitch = SIZES[d_name(d)]
    neck = Part.makeBox(L, NECK_W, NECK_H, V(-L/2, -NECK_W/2, -NECK_H))
    body = Part.makeBox(L, BODY_W, BODY_H, V(-L/2, -BODY_W/2, -NECK_H - BODY_H))
    body = body.makeChamfer(CHAMFER, [e for e in body.Edges if e.BoundBox.XLength > L - 1e-6
                                      and abs(e.BoundBox.ZMax - (-NECK_H - BODY_H)) < 1e-6])
    nut = neck.fuse(body).removeSplitter()
    h = NECK_H + BODY_H
    groove, r_min = thread_groove(d, pitch, -h - 2 * pitch, h + 4 * pitch)
    nut = nut.cut(Part.makeCylinder(r_min, h, V(0, 0, -h)))
    for turn in groove:
        nut = nut.cut(turn)
    for z, flip in ((0, False), (-h, True)):  # 90 deg countersink lead-in, both faces
        r0 = d/2 + THREAD_CHAMFER
        cone = Part.makeCone(r0, 0, r0, V(0, 0, z), V(0, 0, 1 if flip else -1))
        nut = nut.cut(cone)
    return nut.removeSplitter()

d_name = lambda d: f"M{d:g}"
for size in SIZES:
    d = float(size[1:])
    name = f"TNut_2020_Slot6_Sliding_{size}"
    doc = App.newDocument(name)
    o = doc.addObject("Part::Feature", name); o.Shape = make_tnut(d)
    if hasattr(o, "ViewObject") and o.ViewObject: o.ViewObject.ShapeColor = (0.75, 0.76, 0.78)
    doc.recompute()
    fn = os.path.join(OUT, name)
    doc.saveAs(fn + ".FCStd")
    Part.export([o], fn + ".step")
    import Mesh; Mesh.export([o], fn + ".stl")
    s = o.Shape
    print(size, "valid" if s.isValid() else "INVALID", len(s.Solids), round(s.Volume, 1), s.BoundBox)
