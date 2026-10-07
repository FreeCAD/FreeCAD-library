"""Panasonic Toughbook CF-19 — FreeCAD assembly with a revolute lid hinge.

Run headless:  freecad.cmd cf19_toughbook.py
Produces cf19_toughbook.FCStd.  Open it in FreeCAD (Assembly workbench):
drag the lid, or edit Joints > HingeJoint (Offset / angle limits) to open/close it.

Overall size closed ~271 x 216 x 49 mm (W x D x H).  Axes: X = width,
Y = depth (front edge at Y=0, hinge at rear), Z = up.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
import Part
from fcutil import (V, box, rbox, rbox_c, cyl, fuse, cut, compound, text, part, feat, save,
                    dump_mesh, set_vp_proxy, HERE)

OUT = os.path.join(HERE, "cf19_toughbook.FCStd")

# ---- colours
SILVER = (0.66, 0.67, 0.69)
SILVER_D = (0.55, 0.56, 0.58)
RUBBER = (0.12, 0.12, 0.13)
KEYC = (0.16, 0.16, 0.17)
GLASS = (0.04, 0.06, 0.10)
GREEN = (0.1, 0.9, 0.3)
METAL = (0.78, 0.78, 0.80)
WHITE = (0.92, 0.92, 0.92)

# ---- main dimensions
W, D = 271.0, 204.0          # body footprint (handle + hinge add to depth)
HB = 30.0                    # base height
LZ0, LZ1 = 31.0, 49.0        # lid shell z range (closed)
AXIS_Y, AXIS_Z = D, 40.0     # hinge axis (parallel to X)
KR = 7.0                     # knuckle radius
CX = W / 2
# base knuckles [95,115] and [156,176]; lid knuckle [115,156]
BK = [(95.0, 115.0), (156.0, 176.0)]
LK = (115.0, 156.0)

doc = App.newDocument("CF19_Toughbook")
asm = doc.addObject("Assembly::AssemblyObject", "Assembly")
asm.Label = "CF-19 Toughbook"
joints = asm.newObject("Assembly::JointGroup", "Joints")

# ======================================================================
# BASE
# ======================================================================
base = part(doc, "Base", asm, "Base")

shell = rbox(0, 0, 0, W, D, HB, r=14, r_top=2.0, r_bot=3.0)
# keyboard well
kb_x0, kb_x1, kb_y0, kb_y1 = 17.0, W - 17.0, 99.0, 198.0
shell = cut(shell, [
    rbox(kb_x0, kb_y0, HB - 3, kb_x1 - kb_x0, kb_y1 - kb_y0, 5, r=3),
    # touchpad + button recesses
    rbox_c(CX, 62, HB - 1.0, 56, 40, 3, r=3),
    rbox_c(CX, 34, HB - 1.0, 56, 11, 3, r=2),
    # LED window strip
    rbox_c(222, 86, HB - 0.6, 44, 6, 2, r=1.5),
    # port-door recesses on sides
    box(-1, 38, 5, 1.6, 54, 20), box(-1, 108, 5, 1.6, 54, 20),
    box(W - 0.6, 55, 5, 1.6, 90, 20),
])
feat(doc, base, "BaseShell", shell, SILVER, "Base shell")

# keyboard: 6 rows, 13 units wide
pitch = 18.0
rows = [
    (191.0, 8.0, [1] * 13),
    (178.0, 14.5, [1] * 13),
    (161.0, 14.5, [1.5] + [1] * 10 + [1.5]),
    (144.0, 14.5, [1.75] + [1] * 10 + [1.25]),
    (127.0, 14.5, [2.25] + [1] * 9 + [1.75]),
    (110.0, 14.5, [1, 1, 1, 1, 5, 1, 1, 1, 1]),
]
keys = []
x_start = CX - 13 * pitch / 2
for yc, kd, units in rows:
    x = x_start
    for u in units:
        kw = u * pitch - 2.4
        keys.append(rbox_c(x + u * pitch / 2, yc, HB - 3, kw, kd, 2.3, r=1.2, r_top=0.5))
        x += u * pitch
feat(doc, base, "Keyboard", compound(keys), KEYC, "Keyboard")
feat(doc, base, "KeyboardTray", box(kb_x0 + 1, kb_y0 + 1, HB - 3.2, kb_x1 - kb_x0 - 2,
                                       kb_y1 - kb_y0 - 2, 0.3), RUBBER, "Keyboard tray")

# touchpad + buttons
feat(doc, base, "Touchpad", rbox_c(CX, 62, HB - 1.0, 54, 38, 0.6, r=2.5), (0.22, 0.22, 0.23))
feat(doc, base, "TouchpadButtons", compound([
    rbox_c(CX - 13.75, 34, HB - 1.0, 26, 9, 0.8, r=1.5),
    rbox_c(CX + 13.75, 34, HB - 1.0, 26, 9, 0.8, r=1.5)]), RUBBER, "Touchpad buttons")

# status LEDs
feat(doc, base, "LEDWindow", rbox_c(222, 86, HB - 0.6, 44, 6, 0.3, r=1.5), GLASS, "LED window")
feat(doc, base, "LEDs", compound([cyl(1.0, 0.4, (206 + i * 8, 86, HB - 0.4)) for i in range(5)]),
     GREEN, "Status LEDs")

# side port doors with slide latches
doors = []
for y0, ln in ((38, 54), (108, 54)):
    doors.append(rbox(-0.9, y0 + 0.5, 5.5, 1.4, ln - 1, 19, r=0))
    doors.append(rbox(-1.8, y0 + ln / 2 - 6, 12, 1.2, 12, 5, r=0))
doors.append(rbox(W - 0.5, 55.5, 5.5, 1.4, 89, 19, r=0))
doors.append(rbox(W + 0.5, 100 - 6, 12, 1.2, 12, 5, r=0))
feat(doc, base, "PortDoors", compound(doors), SILVER_D, "Port doors")

# corner bumpers (base)
def bumpers(z0, h, grow=1.6, size=34.0, r=15.5):
    outer = rbox(-grow, -grow, z0, W + 2 * grow, D + 2 * grow, h, r=r, r_top=1.5, r_bot=1.5)
    corners = [box(-5, -5, z0 - 1, size, size, h + 2), box(W - size + 5, -5, z0 - 1, size, size, h + 2),
               box(-5, D - size + 5, z0 - 1, size, size, h + 2),
               box(W - size + 5, D - size + 5, z0 - 1, size, size, h + 2)]
    return compound([outer.common(c) for c in corners])


feat(doc, base, "BaseBumpers", bumpers(0.0, HB - 1.0), RUBBER, "Corner bumpers")

# carrying handle on the front edge
handle = fuse([
    rbox(68, -15, 8, W - 136, 9, 13, r=4, r_top=2, r_bot=2),
    rbox(68, -15, 8, 12, 17, 13, r=4, r_top=2, r_bot=2),
    rbox(W - 80, -15, 8, 12, 17, 13, r=4, r_top=2, r_bot=2),
])
feat(doc, base, "Handle", handle, RUBBER, "Carry handle")

# rubber feet
feat(doc, base, "Feet", compound([cyl(5, 1.2, (x, y, -1.2)) for x in (30, W - 30)
                                   for y in (25, D - 25)]), RUBBER, "Feet")

# hinge knuckles on the base (with support blocks)
bh = []
for x0, x1 in BK:
    bh.append(box(x0, AXIS_Y - KR, HB - 4, x1 - x0, 2 * KR, AXIS_Z - (HB - 4)))
    bh.append(cyl(KR, x1 - x0, (x0, AXIS_Y, AXIS_Z), (1, 0, 0)))
base_hinge = feat(doc, base, "BaseHinge", fuse(bh), RUBBER, "Hinge knuckles (base)")

# ======================================================================
# LID  (modelled closed, in the same global frame)
# ======================================================================
lid = part(doc, "Lid", asm, "Lid")

lshell = rbox(0, 0, LZ0, W, D, LZ1 - LZ0, r=14, r_top=3.0, r_bot=1.0)
scr = (32.0, 25.0, 207.0, 155.0)  # x, y, w, h — 10.4" 4:3 panel
lshell = cut(lshell, [
    box(scr[0], scr[1], LZ0 - 1, scr[2], scr[3], 2.5),
    # notches clearing the base knuckles
    box(BK[0][0] - 0.6, AXIS_Y - KR - 1.0, LZ0 - 1, BK[0][1] - BK[0][0] + 0.6, 2 * KR + 2, 20),
    box(BK[1][0], AXIS_Y - KR - 1.0, LZ0 - 1, BK[1][1] - BK[1][0] + 0.6, 2 * KR + 2, 20),
])
feat(doc, lid, "LidShell", lshell, SILVER, "Lid shell")

# raised panel + branding on the lid top
feat(doc, lid, "LidPanel", rbox(34, 28, LZ1, W - 68, 148, 0.6, r=8, r_top=0.3), SILVER_D,
     "Lid panel")
feat(doc, lid, "LidLogo", compound([
    # rotated 180 deg so the branding reads correctly when the lid is open
    text("Panasonic", 15, CX, 110, LZ1 + 0.6, 0.4, rot=((CX, 110, 0), (0, 0, 1), 180)),
    text("TOUGHBOOK", 8, CX, 45, LZ1 + 0.6, 0.4, rot=((CX, 45, 0), (0, 0, 1), 180))]),
    WHITE, "Lid branding")

# bezel (underside, faces the keyboard when closed) and screen
bezel = rbox(6, 6, LZ0 - 0.8, W - 12, D - 12 - 2 * KR, 0.8, r=8)
bezel = cut(bezel, box(scr[0], scr[1], LZ0 - 2, scr[2], scr[3], 4))
feat(doc, lid, "Bezel", bezel, RUBBER, "Screen bezel")
feat(doc, lid, "Screen", box(scr[0] + 0.5, scr[1] + 0.5, LZ0 + 0.6, scr[2] - 1, scr[3] - 1, 0.8),
     GLASS, "Touchscreen")

feat(doc, lid, "LidBumpers", bumpers(LZ0 - 0.5, LZ1 - LZ0 + 1.0), RUBBER, "Corner bumpers")

# front latch
feat(doc, lid, "Latch", fuse([
    rbox_c(CX, -1.0, LZ0 + 4, 36, 4, 11, r=1.5),
    rbox_c(CX, -3.2, LZ0 + 7, 14, 2, 5, r=0.8)]), RUBBER, "Lid latch")

# lid hinge knuckle
lid_hinge = feat(doc, lid, "LidHinge", cyl(KR, LK[1] - LK[0], (LK[0], AXIS_Y, AXIS_Z), (1, 0, 0)),
                 METAL, "Hinge knuckle (lid)")

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


ground = joints.newObject("App::FeaturePython", "GroundedBase")
JointObject.GroundedJoint(ground, base)
ground.Label = "Grounded (Base)"
set_vp_proxy(ground.Name, "JointObject", "ViewProviderGroundedJoint")

hinge = joints.newObject("App::FeaturePython", "HingeJoint")
JointObject.Joint(hinge, JointObject.JointTypes.index("Revolute"))
hinge.Label = "Lid hinge (revolute)"
set_vp_proxy(hinge.Name, "JointObject", "ViewProviderJoint")

pivot = V(LK[0], AXIS_Y, AXIS_Z)
e_base = circle_edge(base_hinge, pivot, KR)
e_lid = circle_edge(lid_hinge, pivot, KR)
hinge.Proxy.setJointConnectors(hinge, [
    [base, ["BaseHinge." + e_base, "BaseHinge." + e_base]],
    [lid, ["LidHinge." + e_lid, "LidHinge." + e_lid]],
])
doc.recompute()

OPEN_ANGLE = float(os.environ.get("CF19_OPEN", "105"))
lid.Placement = App.Placement(V(0, 0, 0), App.Rotation(V(1, 0, 0), -OPEN_ANGLE),
                              V(0, AXIS_Y, AXIS_Z))
res = asm.solve()
doc.recompute()
print("solve ->", res, "lid placement", lid.Placement)

# ---- simulation: close the lid and open it again (Assembly > Simulation, then Run)
# motion angle is the absolute hinge angle in radians (0 = closed, negative = open)
import builtins
import types
import UtilsAssembly

if not App.GuiUp:  # the module subclasses QtCore.QObject at import time
    builtins.QtCore = types.SimpleNamespace(QObject=object)
from CommandCreateSimulation import Simulation, Motion

sim = UtilsAssembly.getSimulationGroup(asm).newObject("App::FeaturePython", "LidSimulation")
Simulation(sim)
sim.Label = "Close and open lid"
sim.bTimeEnd = 4.0
sim.cTimeStepOutput = 0.04
motion = asm.newObject("App::FeaturePython", "LidMotion")
Motion(motion, "Angular", [hinge, [""]],
       "-%.4f*(1+cos(pi*time/2))/2" % math.radians(OPEN_ANGLE))
motion.Label = "Lid swing"
sim.Group = [motion]
set_vp_proxy(sim.Name, "CommandCreateSimulation", "ViewProviderSimulation")
set_vp_proxy(motion.Name, "CommandCreateSimulation", "ViewProviderMotion")
doc.recompute()

save(doc, OUT, hidden=(motion.Name,))
dump_mesh(doc, os.path.join(HERE, "preview", "cf19_toughbook.json"))
