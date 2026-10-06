"""Linksys WRT54G wireless-G broadband router — FreeCAD assembly with swivelling antennas.

Run headless:  freecad.cmd linksys_wrt54g.py   ->  linksys_wrt54g.FCStd
Each antenna is a separate part on a Revolute joint (knuckle axis parallel to X),
so it can be tilted forward/back by dragging it in the Assembly workbench.

Case ~186 x 200 x 48 mm (W x D x H incl. feet).  Axes: X = width, Y = depth
(front LED panel at Y=0, ports/antennas at the rear), Z = up.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
import Part
from fcutil import (V, box, rbox, rbox_c, cyl, cone, sphere, fuse, cut, compound, text, part,
                    feat, save, dump_mesh, set_vp_proxy, HERE)

OUT = os.path.join(HERE, "linksys_wrt54g.FCStd")

BLUE = (0.10, 0.22, 0.50)
BLACK = (0.10, 0.10, 0.11)
DARK = (0.18, 0.18, 0.19)
SMOKE = (0.05, 0.05, 0.07)
GREEN = (0.15, 0.95, 0.35)
AMBER = (1.0, 0.65, 0.1)
SILVER = (0.80, 0.80, 0.82)
GOLD = (0.85, 0.70, 0.30)
WHITE = (0.92, 0.92, 0.92)

W, D = 186.0, 200.0
Z_FEET, Z_SPLIT, Z_TOP = 5.0, 22.0, 44.0
# front bezel leans forward: bottom edge at y=7, top edge at y=0
FB_Y0, FB_Y1 = 7.0, 0.0
SLANT = math.degrees(math.atan((FB_Y0 - FB_Y1) / (Z_TOP - Z_FEET)))

# antennas: connector on the rear face, knuckle axis parallel to X
ANT_Z = 32.0
ANT_Y = D + 14.0
ANT_R = 6.0
ANT_X = (14.0, W - 14.0)

doc = App.newDocument("WRT54G")
asm = doc.addObject("Assembly::AssemblyObject", "Assembly")
asm.Label = "Linksys WRT54G"
joints = asm.newObject("Assembly::JointGroup", "Joints")


def yz_prism(pts, x0, length):
    """Prism from a (y, z) polygon, extruded along +X from x0."""
    w = Part.makePolygon([V(x0, y, z) for y, z in pts + [pts[0]]])
    return Part.Face(w).extrude(V(length, 0, 0))


def on_front(shape):
    """Map geometry built against a vertical face at y=FB_Y0 onto the slanted bezel."""
    s = shape.copy()
    s.rotate(V(0, FB_Y0, Z_FEET), V(1, 0, 0), SLANT)
    return s


def front_text(s, size, cx, zc, y=FB_Y0, height=0.4):
    t = text(s, size, cx, 0, 0, height)
    t.rotate(V(0, 0, 0), V(1, 0, 0), 90)  # now faces -Y, reads along +X
    t.translate(V(0, y, zc))
    return t


# ======================================================================
# BODY
# ======================================================================
body = part(doc, "Body", asm, "Router body")

outline = rbox(0, 0, -1, W, D, 60, r=9)
slope = (FB_Y1 - FB_Y0) / (Z_TOP - Z_FEET)
front_cutter = yz_prism([(-20, -1), (FB_Y0 + slope * (-1 - Z_FEET), -1),
                         (FB_Y0 + slope * (60 - Z_FEET), 60), (-20, 60)], -1, W + 2)
bezel = yz_prism([(FB_Y0, Z_FEET), (18, Z_FEET), (18, Z_TOP), (FB_Y1, Z_TOP)], 0, W).common(outline)

lower = rbox(0, 0, Z_FEET, W, D, Z_SPLIT - Z_FEET, r=9, r_bot=2.5)
lower = cut(lower, front_cutter)
# rear ports (viewed from behind, right to left): reset, Internet, 4..1 LAN, power
ports = [(150.0, "Internet")] + [(124.0 - i * 17.0, "LAN%d" % (4 - i)) for i in range(4)]
port_cuts = [box(x - 7.2, D - 15, 8.5, 14.4, 16, 12.0) for x, _ in ports]
lower = cut(lower, port_cuts + [
    cyl(4.2, 16, (40, D - 15, 15), (0, 1, 0)),           # power jack
    cyl(1.6, 10, (170, D - 9, 15), (0, 1, 0)),           # reset hole
] + [box(-1, 40 + i * 9, 10, 2.5, 4, 8) for i in range(14)]  # side vents
  + [box(W - 1.5, 40 + i * 9, 10, 2.5, 4, 8) for i in range(14)])
feat(doc, body, "LowerShell", lower, BLACK, "Lower shell")

top = rbox(0, 0, Z_SPLIT, W, D, Z_TOP - Z_SPLIT, r=9, r_top=6)
top = cut(top, [bezel, front_cutter]
          # stacking grooves and rear vents
          + [box(x, 30, Z_TOP - 1.2, 6, 150, 3) for x in (40, W - 46)]
          + [rbox_c(W / 2 - 50 + i * 10, 165, Z_TOP - 2.5, 3.5, 34, 4, r=1.5) for i in range(11)])
feat(doc, body, "TopShell", top, BLUE, "Top shell")
feat(doc, body, "VentFloor", box(W / 2 - 54, 146, Z_TOP - 3, 108, 38, 0.6), SMOKE, "Vent floor")
feat(doc, body, "FrontBezel", bezel, DARK, "Front bezel")

# LED window + LEDs + branding on the slanted front
led_names = ["Power", "DMZ", "WLAN", "1", "2", "3", "4", "Internet"]
feat(doc, body, "LEDWindow", on_front(rbox(96, FB_Y0 - 0.6, 22, 80, 0.6, 12, r=2)), SMOKE,
     "LED window")
leds = []
for i, n in enumerate(led_names):
    leds.append(box(101 + i * 9.6, FB_Y0 - 1.0, 27, 3.5, 0.5, 1.8))
feat(doc, body, "LEDsGreen", on_front(compound([l for i, l in enumerate(leds) if i != 1])), GREEN,
     "LEDs")
feat(doc, body, "LEDDMZ", on_front(leds[1]), AMBER, "DMZ LED")
feat(doc, body, "FrontText", on_front(compound([
    front_text("LINKSYS", 8.5, 45, 31),
    front_text("Wireless-G Broadband Router", 3.0, 45, 22),
    front_text("WRT54G", 3.5, 136, 15),
])), WHITE, "Front branding")
feat(doc, body, "TopLogo", text("CISCO SYSTEMS", 4.5, W / 2, 40, Z_TOP, 0.3), SILVER, "Top logo")

# port internals
feat(doc, body, "PortInserts", compound(
    [box(x - 7.2, D - 15, 8.5, 14.4, 3, 12.0) for x, _ in ports]
    + [box(x - 4.5, D - 12, 18.5, 9, 6, 1.0) for x, _ in ports]), DARK, "RJ45 jacks")
feat(doc, body, "PortContacts", compound(
    [box(x - 3.8 + k * 1.02, D - 12, 18.0, 0.4, 7, 0.5) for x, _ in ports for k in range(8)]),
    GOLD, "RJ45 contacts")
feat(doc, body, "PowerJack", fuse([cyl(1.0, 10, (40, D - 14, 15), (0, 1, 0)),
                                    box(36, D - 15, 11, 8, 1.5, 8).cut(cyl(4.2, 3, (40, D - 16, 15), (0, 1, 0)))]),
     SILVER, "Power jack")
feat(doc, body, "Feet", compound([cyl(6, Z_FEET + 0.5, (x, y, 0)) for x in (22, W - 22)
                                   for y in (22, D - 22)]), BLACK, "Rubber feet")

# antenna connectors (RP-TNC) and the fixed half of each knuckle
conns, knuckles = [], []
for side, xa in zip((-1, 1), ANT_X):
    conns.append(cyl(4.6, ANT_Y - D + 2, (xa, D - 2, ANT_Z), (0, 1, 0)))
    conns.append(cyl(6.0, 3, (xa, D - 1, ANT_Z), (0, 1, 0)))  # hex nut, simplified
    x0 = xa - 6 if side < 0 else xa
    knuckles.append(cyl(ANT_R, 6, (x0, ANT_Y, ANT_Z), (1, 0, 0)))
feat(doc, body, "AntennaConnectors", compound(conns), GOLD, "RP-TNC connectors")
body_knuckles = feat(doc, body, "BodyKnuckles", compound(knuckles), BLACK, "Antenna knuckle bases")

# ======================================================================
# ANTENNAS (modelled vertical)
# ======================================================================
ant_parts, ant_knuckles = [], []
for side, xa, tag in zip((-1, 1), ANT_X, ("L", "R")):
    ap = part(doc, "Antenna" + tag, asm, "Antenna " + ("left" if tag == "L" else "right"))
    x0 = xa if side < 0 else xa - 6
    k = feat(doc, ap, "Knuckle" + tag, cyl(ANT_R, 6, (x0, ANT_Y, ANT_Z), (1, 0, 0)), DARK,
             "Knuckle " + tag)
    z0 = ANT_Z + ANT_R
    whip = fuse([
        cyl(5.5, 22, (xa, ANT_Y, z0)),
        cone(5.5, 4.2, 82, (xa, ANT_Y, z0 + 22)),
        cyl(4.2, 4, (xa, ANT_Y, z0 + 104)),
        sphere(4.2, (xa, ANT_Y, z0 + 108)),
    ])
    feat(doc, ap, "Whip" + tag, whip, BLACK, "Whip " + tag)
    feat(doc, ap, "Ring" + tag, cyl(5.8, 1.2, (xa, ANT_Y, z0 + 18)), SILVER, "Trim ring " + tag)
    ant_parts.append(ap)
    ant_knuckles.append(k)

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


ground = joints.newObject("App::FeaturePython", "GroundedBody")
JointObject.GroundedJoint(ground, body)
ground.Label = "Grounded (Body)"
set_vp_proxy(ground.Name, "JointObject", "ViewProviderGroundedJoint")

for xa, ap, k, tag in zip(ANT_X, ant_parts, ant_knuckles, ("L", "R")):
    j = joints.newObject("App::FeaturePython", "AntennaJoint" + tag)
    JointObject.Joint(j, JointObject.JointTypes.index("Revolute"))
    j.Label = "Antenna %s swivel (revolute)" % tag
    set_vp_proxy(j.Name, "JointObject", "ViewProviderJoint")
    pivot = V(xa, ANT_Y, ANT_Z)
    eb = circle_edge(body_knuckles, pivot, ANT_R)
    ea = circle_edge(k, pivot, ANT_R)
    j.Proxy.setJointConnectors(j, [
        [body, ["BodyKnuckles." + eb, "BodyKnuckles." + eb]],
        [ap, [k.Name + "." + ea, k.Name + "." + ea]],
    ])
doc.recompute()
print("solve ->", asm.solve(), [a.Placement for a in ant_parts])

save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "linksys_wrt54g.json"))
