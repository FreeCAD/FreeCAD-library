"""Logitech C920 HD Pro webcam — FreeCAD assembly with a revolute tilt hinge.

Run headless:  freecad.cmd logitech_c920.py   ->  logitech_c920.FCStd
The clip is grounded; the camera tilts about the hinge (Joints > TiltJoint).
Drag the camera in the Assembly workbench to tilt it.

Camera body ~94 x 24 x 29 mm (W x D x H), stadium-shaped front.
Axes: X = width, Y = depth (lens faces -Y), Z = up.  Hinge axis parallel to X.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
import Part
from fcutil import (V, box, rbox, rbox_c, cyl, cone, fuse, cut, compound, text, part, feat,
                    save, dump_mesh, set_vp_proxy, HERE)

OUT = os.path.join(HERE, "logitech_c920.FCStd")

BLACK_GLOSS = (0.05, 0.05, 0.06)
BLACK = (0.10, 0.10, 0.11)
GREY = (0.32, 0.33, 0.35)
SILVER = (0.72, 0.73, 0.75)
GLASS = (0.02, 0.03, 0.07)
LENSBLUE = (0.10, 0.14, 0.30)
WHITE = (0.90, 0.90, 0.90)
LEDC = (0.95, 0.95, 0.85)
RUBBER = (0.15, 0.15, 0.15)
BRASS = (0.70, 0.62, 0.35)

W, D, H = 94.0, 24.0, 29.0
R = H / 2
ZC = 18.0 + R               # body centre height (body sits above the hinge)
Y0 = -D / 2                 # front face
PIV = V(0, 3.0, 9.0)        # tilt hinge axis point (axis along X)
KR = 3.5                    # hinge knuckle radius


def stadium(w, h, y0, depth, zc, r=None):
    """Stadium (pill) prism: w wide in X, h tall in Z, extruded +Y from y0."""
    r = h / 2 if r is None else r
    core = box(-w / 2 + r, y0, zc - h / 2, w - 2 * r, depth, h)
    return fuse([core, cyl(r, depth, (-w / 2 + r, y0, zc), (0, 1, 0)),
                 cyl(r, depth, (w / 2 - r, y0, zc), (0, 1, 0))])


def front_text(s, size, x, z, y=Y0, height=0.15):
    return text(s, size, x, y, z, height, rot=((x, y, z), (1, 0, 0), 90))


doc = App.newDocument("Logitech_C920")
asm = doc.addObject("Assembly::AssemblyObject", "Assembly")
asm.Label = "Logitech C920"
joints = asm.newObject("Assembly::JointGroup", "Joints")

# ======================================================================
# CAMERA
# ======================================================================
cam = part(doc, "Camera", asm, "Camera")

# rear housing (grey/black matte) and glossy front bezel
rear = stadium(W, H, Y0 + 6, D - 6, ZC)
rear = rear.makeFillet(2.5, [e for e in rear.Edges
                             if all(abs(v.Y - (Y0 + D)) < 1e-6 for v in e.Vertexes)])
feat(doc, cam, "RearHousing", rear, GREY, "Rear housing")

front = stadium(W, H, Y0, 6.0, ZC)
front = front.makeFillet(1.8, [e for e in front.Edges
                               if all(abs(v.Y - Y0) < 1e-6 for v in e.Vertexes)])
# lens bore + mic + LED holes
LX = 0.0
front = cut(front, [cyl(8.2, 8, (LX, Y0 - 1, ZC), (0, 1, 0)),
                    cyl(0.9, 3, (-37.5, Y0 - 1, ZC), (0, 1, 0)),
                    cyl(0.9, 3, (37.5, Y0 - 1, ZC), (0, 1, 0)),
                    cyl(0.8, 3, (-14.0, Y0 - 1, ZC + 8.5), (0, 1, 0))])
feat(doc, cam, "FrontBezel", front, BLACK_GLOSS, "Front bezel (gloss)")

# lens: Zeiss trim ring, barrel, glass
ring = cut(cyl(9.2, 1.4, (LX, Y0 - 0.9, ZC), (0, 1, 0)), cyl(6.6, 3, (LX, Y0 - 2, ZC), (0, 1, 0)))
feat(doc, cam, "LensRing", ring, SILVER, "Lens trim ring (Carl Zeiss)")
barrel = cut(cyl(8.1, 6.0, (LX, Y0 + 0.2, ZC), (0, 1, 0)), cyl(5.0, 7, (LX, Y0, ZC), (0, 1, 0)))
feat(doc, cam, "LensBarrel", barrel, BLACK, "Lens barrel")
feat(doc, cam, "LensGlass", cyl(5.0, 0.6, (LX, Y0 + 2.6, ZC), (0, 1, 0)), LENSBLUE, "Lens glass")
feat(doc, cam, "LensRingText", compound([
    front_text("CARL ZEISS TESSAR", 1.1, LX, ZC + 10.4, y=Y0 - 0.9),
    front_text("HD 1080p", 2.6, 30.0, ZC - 9.0)]), WHITE, "Front lettering")

# mic grilles (perforated dark discs behind the holes) and LED
mics = []
for sx in (-37.5, 37.5):
    mics.append(cyl(2.4, 0.4, (sx, Y0 - 0.4, ZC), (0, 1, 0)))
mic_holes = [cyl(0.35, 1, (sx + dx, Y0 - 0.8, ZC + dz), (0, 1, 0))
             for sx in (-37.5, 37.5) for dx in (-1.3, 0, 1.3) for dz in (-1.3, 0, 1.3)]
feat(doc, cam, "MicGrilles", cut(fuse(mics), mic_holes), BLACK, "Microphone grilles (stereo)")
feat(doc, cam, "LED", cyl(0.8, 0.5, (-14.0, Y0 - 0.3, ZC + 8.5), (0, 1, 0)), LEDC, "Activity LED")
feat(doc, cam, "Logo", front_text("logitech", 3.4, -27.0, ZC - 9.0), WHITE, "Logitech logo")

# cable exits from the rear left of the body
feat(doc, cam, "CableBoot", cyl(2.6, 9, (-W / 2 + 12, Y0 + D - 0.5, ZC - 4), (0, 1, 0)),
     BLACK, "Cable strain relief")
feat(doc, cam, "Cable", cyl(1.8, 14, (-W / 2 + 12, Y0 + D + 8.5, ZC - 4), (0, 1, 0)),
     BLACK, "USB cable (stub)")

# hinge knuckles on the camera underside: x in [-16,-8] and [8,16]
ck = []
for x0 in (-16.0, 8.0):
    ck.append(cyl(KR, 8.0, (x0, PIV.y, PIV.z), (1, 0, 0)))
    ck.append(box(x0, PIV.y - KR, PIV.z, 8.0, 2 * KR, ZC - R + 2 - PIV.z))
cam_hinge = feat(doc, cam, "CameraKnuckles", fuse(ck), BLACK, "Hinge knuckles (camera)")

# ======================================================================
# CLIP / STAND
# ======================================================================
clip = part(doc, "Clip", asm, "Monitor clip")

clip_k = feat(doc, clip, "ClipKnuckle", cyl(KR, 16.0, (-8.0, PIV.y, PIV.z), (1, 0, 0)), BLACK,
              "Hinge knuckle (clip)")
# neck from knuckle down to top plate
neck = rbox(-8, PIV.y - KR, 0, 16, 2 * KR, PIV.z, r=1.0)
# top plate that rests on the monitor (with 1/4"-20 tripod insert underneath)
plate = rbox(-15, -10, -4, 30, 32, 4, r=4, r_top=0.8)
plate = cut(plate, cyl(3.4, 4, (0, 4, -5)))
# front lip that drops in front of the monitor bezel
lip = rbox(-15, -10, -14, 30, 3, 10.5, r=1.0)
feat(doc, clip, "ClipBody", fuse([neck, plate, lip]), BLACK, "Clip body")
# tripod thread insert (1/4"-20 UNC: major dia 6.35 mm)
insert = cut(cyl(3.4, 3.8, (0, 4, -3.9)), cyl(3.175, 4, (0, 4, -4.5)))
feat(doc, clip, "TripodInsert", insert, BRASS, "1/4\"-20 tripod insert")

# folding rear leg, hinged at the back of the plate, angled down behind the monitor
leg = rbox(-15, 0, -45, 30, 3, 45, r=1.5)
leg.rotate(V(0, 0, 0), V(1, 0, 0), -12)
leg.translate(V(0, 22, -1.5))
feat(doc, clip, "RearLeg", leg, BLACK, "Folding rear leg")
feat(doc, clip, "LegHinge", cyl(2.0, 30, (-15, 22.5, -2.2), (1, 0, 0)), GREY, "Leg hinge pin")
feet = [rbox(-13, -10.5, -14.6, 26, 3.5, 1.2, r=0.8)]
foot = rbox(-13, -0.5, -45.8, 26, 4, 1.4, r=0.8)
foot.rotate(V(0, 0, 0), V(1, 0, 0), -12)
foot.translate(V(0, 22, -1.5))
feet.append(foot)
feat(doc, clip, "RubberPads", compound(feet), RUBBER, "Rubber pads")

doc.recompute()

# ======================================================================
# JOINTS
# ======================================================================
import JointObject


def circle_edge(obj, center, radius):
    for i, e in enumerate(obj.Shape.Edges):
        c = e.Curve
        if isinstance(c, Part.Circle) and abs(c.Radius - radius) < 1e-6 \
                and (c.Center - center).Length < 1e-6:
            return "Edge%d" % (i + 1)
    raise RuntimeError("no circle edge on %s at %s" % (obj.Name, center))


ground = joints.newObject("App::FeaturePython", "GroundedClip")
JointObject.GroundedJoint(ground, clip)
ground.Label = "Grounded (Clip)"
set_vp_proxy(ground.Name, "JointObject", "ViewProviderGroundedJoint")

tilt = joints.newObject("App::FeaturePython", "TiltJoint")
JointObject.Joint(tilt, JointObject.JointTypes.index("Revolute"))
tilt.Label = "Camera tilt (revolute)"
set_vp_proxy(tilt.Name, "JointObject", "ViewProviderJoint")

pivot = V(8.0, PIV.y, PIV.z)
e_clip = circle_edge(clip_k, pivot, KR)
e_cam = circle_edge(cam_hinge, pivot, KR)
tilt.Proxy.setJointConnectors(tilt, [
    [clip, ["ClipKnuckle." + e_clip, "ClipKnuckle." + e_clip]],
    [cam, ["CameraKnuckles." + e_cam, "CameraKnuckles." + e_cam]],
])
doc.recompute()

TILT = float(os.environ.get("C920_TILT", "-8"))  # degrees, negative = lens tips down
cam.Placement = App.Placement(V(0, 0, 0), App.Rotation(V(1, 0, 0), TILT), PIV)
res = asm.solve()
doc.recompute()
print("solve ->", res, "camera placement", cam.Placement)

save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "logitech_c920.json"), tol=0.1)
