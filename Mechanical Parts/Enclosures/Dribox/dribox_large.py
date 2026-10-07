"""DRiBOX Large (black) — IP55 weatherproof outdoor connection box, 400 x 310 x 145 mm.

Run headless:  freecad.cmd dribox_large.py   ->  dribox_large.FCStd
Based on the Amazon UK listing B003O2X6T8: tapered tub, internal 330 x 230 x 140,
moulded 200 mm handles on the short ends, 1 input + 4 output cable channels all
on one long side (each with a silicone seal and an external cable duct); ribbed
"roof style" lid with matching seal tongues, silicone rim gasket and clips over
the handles at both ends.

Assembly: the base is grounded; the lid has no hinge — it lifts straight off.
It sits on a vertical Slider joint (drag it up/down; suppress LidSlider to move
it freely) and the "Put lid on and lift off" simulation animates it.

Box sitting flat, centred on the origin: X = length (400), Y = width (310), Z = up.
"""
import builtins
import math
import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
import Part
from fcutil import (V, box, rbox_c, cyl, fuse, cut, compound, text, part, feat, save, dump_mesh,
                    set_vp_proxy, HERE)

OUT = os.path.join(HERE, "dribox_large.FCStd")

BLACK = (0.08, 0.08, 0.09)
SEAL = (0.20, 0.20, 0.21)      # silicone seals / gasket
WHITE = (0.95, 0.95, 0.95)
GREEN = (0.13, 0.62, 0.27)

# ---- dimensions
T = 4.0                          # tub wall
ZT = 121.0                       # top of the tub rim
IN_TOP = (330.0, 230.0)          # internal size at the top
OUT_BOT = (310.0, 210.0)         # external size at the floor (walls are drafted)
FL = (350.0, 290.0)              # rim flange outline
FL_Z0 = 116.0                    # flange underside
LIP_Z0 = 106.0                   # bottom of the flange's down-turned lip
HANDLE_X = 195.0                 # handle ledges reach +-HANDLE_X
LID = (360.0, 300.0)             # lid skirt outline
LID_Z0 = 108.0                   # lid skirt bottom
CH_W, CH_R = 16.0, 8.0           # cable channel width / bottom radius
CH_ZC = 107.0                    # channel bottom arc centre
# all five channels are on the front (-Y) long side: input near the left end,
# then the four outputs towards the right end
INPUTS = [-115.0]                      # x of the input channel
OUTPUTS = [18.0, 56.0, 95.0, 134.0]    # x of the 4 output channels
LIFT = float(os.environ.get("DRIBOX_LIFT", "90"))  # saved lid lift height, mm


def rrect_wire(l, w, z, r):
    f = [f for f in rbox_c(0, 0, z, l, w, 1, r=r).Faces
         if abs(f.normalAt(0, 0).z + 1) < 1e-6][0]
    return f.OuterWire


def loft(l0, w0, z0, r0, l1, w1, z1, r1):
    return Part.makeLoft([rrect_wire(l0, w0, z0, r0), rrect_wire(l1, w1, z1, r1)], True, True)


def channel(xc, sy, r=CH_R, w=CH_W, y_in=108.0, y_out=FL[1] / 2 + 4, ztop=ZT + 10):
    """U-notch down from the rim on the long side sy (+1/-1)."""
    y0, y1 = (y_in, y_out) if sy > 0 else (-y_out, -y_in)
    return fuse([box(xc - w / 2, y0, CH_ZC, w, y1 - y0, ztop - CH_ZC),
                 cyl(r, y1 - y0, (xc, y0, CH_ZC), (0, 1, 0))])


chans = [(x, -1) for x in INPUTS + OUTPUTS]

doc = App.newDocument("DRiBOX_Large")
asm = doc.addObject("Assembly::AssemblyObject", "Assembly")
asm.Label = "DRiBOX Large 400x310x145"
joints = asm.newObject("Assembly::JointGroup", "Joints")

# ======================================================================
# BASE
# ======================================================================
base = part(doc, "Base", asm, "Base")

out_top = (IN_TOP[0] + 2 * T, IN_TOP[1] + 2 * T)
tub = loft(OUT_BOT[0], OUT_BOT[1], 0, 26, out_top[0], out_top[1], ZT, 30)

# moulded cable housings down the outside of the front wall: a wide block under
# the input channel and a column under each output; each has a duct, open at the
# bottom, that the cable runs up before entering over the rim
HOUS_Y0, HOUS_Z0 = -(FL[1] / 2 - 3), 22.0
housings = [box(INPUTS[0] - 8, HOUS_Y0, HOUS_Z0, 100, 45, FL_Z0 - HOUS_Z0 + 0.5)]
housings += [box(x - 12, HOUS_Y0, HOUS_Z0, 24, 45, FL_Z0 - HOUS_Z0 + 0.5) for x in OUTPUTS]
tub = fuse([tub] + housings)
tub = cut(tub, [box(x - CH_W / 2, HOUS_Y0 - 1, HOUS_Z0 - 1, CH_W, 22, ZT)
                for x in INPUTS + OUTPUTS])
tub = cut(tub, loft(OUT_BOT[0] - 2 * T, OUT_BOT[1] - 2 * T, T, 22,
                    IN_TOP[0], IN_TOP[1], ZT + 0.01, 26))
flange = cut(rbox_c(0, 0, FL_Z0, FL[0], FL[1], ZT - FL_Z0, r=34),
             rbox_c(0, 0, FL_Z0 - 1, out_top[0] - 2, out_top[1] - 2, 10, r=29))
lip = cut(rbox_c(0, 0, LIP_Z0, FL[0], FL[1], FL_Z0 - LIP_Z0 + 0.5, r=34),
          rbox_c(0, 0, LIP_Z0 - 1, FL[0] - 6, FL[1] - 6, 20, r=31))

# moulded 200 mm handle ledges on the short ends, with a finger slot underneath
handles = []
for s in (-1, 1):
    ln = HANDLE_X - FL[0] / 2 + 8
    hb = rbox_c(s * (HANDLE_X - ln / 2), 0, 110, ln, 200, ZT - 110 - 1.0, r=6)
    hb = cut(hb, rbox_c(s * (HANDLE_X - 9), 0, 109, 12, 170, 7, r=4))
    handles.append(hb)

# drafted ribs on the long sides (clear of the cable housings at the front)
draft = math.degrees(math.atan(((out_top[1] - OUT_BOT[1]) / 2) / ZT))
ribs = []
for sy in (-1, 1):
    for x in ((-120, -60, 0, 60, 120) if sy > 0 else (-150, -15)):
        rb = box(x - 3, -2.5 if sy < 0 else -1.0, 6, 6, 3.5, LIP_Z0 - 8)
        rb.rotate(V(0, 0, 0), V(1, 0, 0), -sy * draft)
        rb.translate(V(0, sy * (OUT_BOT[1] / 2 + 0.5), 0))
        ribs.append(rb)

shell = fuse([tub, flange, lip] + handles + ribs)
shell = cut(shell, [channel(x, sy) for x, sy in chans])
feat(doc, base, "BaseShell", shell, BLACK, "Base (tub)")

# silicone U-seals lining each channel
liners = [cut(channel(x, sy, r=CH_R - 0.05, w=CH_W - 0.1, y_in=110.0, y_out=FL[1] / 2 + 0.5,
                      ztop=ZT),
              channel(x, sy, r=CH_R - 2.2, w=CH_W - 4.4, y_in=100, y_out=FL[1] / 2 + 10))
          for x, sy in chans]
feat(doc, base, "ChannelSeals", compound(liners), SEAL, "Silicone cable seals (base)")

# silicone rim gasket
GASKET = (FL[0] - 4, FL[1] - 4, 32.0)   # outline l, w, corner r
GZ1 = ZT + 1.5                           # gasket top: the lid seats here
gasket = cut(rbox_c(0, 0, ZT, GASKET[0], GASKET[1], 1.5, r=GASKET[2]),
             [rbox_c(0, 0, ZT - 1, out_top[0] + 4, out_top[1] + 4, 4, r=31)]
             + [channel(x, sy) for x, sy in chans])
gasket_obj = feat(doc, base, "Gasket", gasket, SEAL, "Silicone gasket")

# ======================================================================
# LID (modelled closed)
# ======================================================================
lid = part(doc, "Lid", asm, "Lid")

ROOF_Z, TOP_Z = 128.0, 139.0
TOP = (336.0, 258.0)
lid_solid = fuse([
    rbox_c(0, 0, LID_Z0, LID[0], LID[1], ROOF_Z - LID_Z0, r=36),
    loft(LID[0], LID[1], ROOF_Z - 0.01, 36, TOP[0], TOP[1], TOP_Z, 26),
    rbox_c(0, 0, TOP_Z - 0.01, TOP[0], TOP[1], 4.0, r=26, r_top=2),
])
lid_solid = cut(lid_solid, [
    # underside cavity: clears flange and lip, seats on the gasket
    rbox_c(0, 0, LID_Z0 - 1, LID[0] - 6, LID[1] - 6, GZ1 - LID_Z0 + 1, r=33),
    loft(LID[0] - 6, LID[1] - 6, GZ1 - 0.01, 33, TOP[0] - 10, TOP[1] - 10, TOP_Z, 21),
    rbox_c(0, 0, TOP_Z - 0.1, TOP[0] - 10, TOP[1] - 10, 1.1, r=21),
] + [channel(x, sy, w=CH_W + 2, ztop=GZ1) for x, sy in chans])
# clip housings closing over the handle ledges at both ends (double locking)
clips = []
for s in (-1, 1):
    ln = HANDLE_X + 5 - LID[0] / 2 + 8
    cl = rbox_c(s * (HANDLE_X + 5 - ln / 2), 0, LID_Z0 - 2, ln, 90, 134 - LID_Z0, r=6, r_top=3)
    cl = cut(cl, rbox_c(s * (HANDLE_X + 1 - (ln - 6) / 2), 0, LID_Z0 - 3, ln - 6, 82,
                        GZ1 - LID_Z0 + 3, r=4))
    clips.append(cl)
lid_solid = fuse([lid_solid] + clips)
feat(doc, lid, "LidShell", lid_solid, BLACK, "Lid (roof style)")

# silicone tongues that press down into each channel, leaving a cable hole
tongues = []
for x, sy in chans:
    y0, y1 = (110.0, LID[1] / 2) if sy > 0 else (-LID[1] / 2, -110.0)
    tg = box(x - CH_W / 2 + 0.1, y0, CH_ZC + 3.0, CH_W - 0.2, y1 - y0, GZ1 - CH_ZC - 3.0 + 0.5)
    tg = cut(tg, cyl(CH_R - 2.2, y1 - y0 + 2, (x, y0 - 1, CH_ZC), (0, 1, 0)))
    tongues.append(tg)
feat(doc, lid, "LidSeals", compound(tongues), SEAL, "Silicone cable seals (lid)")

# ribs across the top at both ends
TZ = TOP_Z + 4.0
feat(doc, lid, "LidRibs", compound([rbox_c(sx * x, 0, TZ - 0.3, 6, TOP[1] - 30, 2.3, r=2.5,
                                           r_top=1.0)
                                    for sx in (-1, 1) for x in (118, 134, 150)]),
     BLACK, "Lid ribs")

# label
feat(doc, lid, "Label", rbox_c(0, 0, TZ, 200, 120, 0.3, r=6), WHITE, "Label")
feat(doc, lid, "LabelPrint", compound([
    text("DRiBOX", 24, -32, 15, TZ + 0.3, 0.2),
    text("CONNECTIONS MADE SIMPLE", 5.5, -32, -15, TZ + 0.3, 0.2),
    rbox_c(70, 22, TZ + 0.3, 40, 40, 0.2, r=4),
    rbox_c(70, -30, TZ + 0.3, 40, 30, 0.2, r=4)]), GREEN, "Label print")
feat(doc, lid, "LabelText2", compound([
    text("IP55", 10, 70, 22, TZ + 0.5, 0.2),
    text("UK", 9, 70, -30, TZ + 0.5, 0.2)]), WHITE, "Label print (white)")

# seating land under the lid, same outline as the gasket (slider reference)
land = cut(rbox_c(0, 0, GZ1, GASKET[0], GASKET[1], 0.5, r=GASKET[2]),
           rbox_c(0, 0, GZ1 - 1, out_top[0] + 4, out_top[1] + 4, 3, r=31))
land_obj = feat(doc, lid, "SeatLand", land, BLACK, "Seat land (slider reference)")

doc.recompute()

# ======================================================================
# JOINTS — vertical slider: the lid lifts straight off, no rotation
# ======================================================================
import JointObject


def planar_face_vertex(obj, z, normal_z, xy):
    """Planar face at height z with the given normal, plus its vertex at (x, y)."""
    shp = obj.Shape
    for i, f in enumerate(shp.Faces):
        if not isinstance(f.Surface, Part.Plane):
            continue
        if abs(f.normalAt(0, 0).z - normal_z) > 1e-6 or abs(f.CenterOfMass.z - z) > 1e-6:
            continue
        for vx in f.Vertexes:
            if abs(vx.X - xy[0]) < 1e-6 and abs(vx.Y - xy[1]) < 1e-6:
                for k, v2 in enumerate(shp.Vertexes):
                    if v2.Point.isEqual(vx.Point, 1e-6):
                        return "Face%d" % (i + 1), "Vertex%d" % (k + 1)
    raise RuntimeError("no face/vertex on %s at z=%s" % (obj.Name, z))


ground = joints.newObject("App::FeaturePython", "GroundedBase")
JointObject.GroundedJoint(ground, base)
ground.Label = "Grounded (Base)"
set_vp_proxy(ground.Name, "JointObject", "ViewProviderGroundedJoint")

slider = joints.newObject("App::FeaturePython", "LidSlider")
JointObject.Joint(slider, JointObject.JointTypes.index("Slider"))
slider.Label = "Lid lift (slider)"
set_vp_proxy(slider.Name, "JointObject", "ViewProviderJoint")

# gasket top and seat-land underside share an outline; use the vertex where the
# +X short-end straight edge starts on both (no channels there)
ref_xy = (GASKET[0] / 2, -GASKET[1] / 2 + GASKET[2])
fb, vb = planar_face_vertex(gasket_obj, GZ1, 1, ref_xy)
fl, vl = planar_face_vertex(land_obj, GZ1, -1, ref_xy)
slider.Proxy.setJointConnectors(slider, [
    [base, ["Gasket." + fb, "Gasket." + vb]],
    [lid, ["SeatLand." + fl, "SeatLand." + vl]],
])
doc.recompute()

lid.Placement = App.Placement(V(0, 0, LIFT), App.Rotation())
print("solve ->", asm.solve(), lid.Placement)

# ---- simulation: lower the lid on, then lift it off again (starts at the saved lift)
# the motion value is the absolute slider travel in mm (0 = closed)
if not App.GuiUp:  # the module subclasses QtCore.QObject at import time
    builtins.QtCore = types.SimpleNamespace(QObject=object)
import UtilsAssembly
from CommandCreateSimulation import Simulation, Motion

sim = UtilsAssembly.getSimulationGroup(asm).newObject("App::FeaturePython", "LidSimulation")
Simulation(sim)
sim.Label = "Put lid on and lift off"
sim.bTimeEnd = 4.0
sim.cTimeStepOutput = 0.04
motion = asm.newObject("App::FeaturePython", "LidMotion")
Motion(motion, "Linear", [slider, [""]], "%.1f*(1+cos(pi*time/2))/2" % LIFT)
motion.Label = "Lid lift"
sim.Group = [motion]
set_vp_proxy(sim.Name, "CommandCreateSimulation", "ViewProviderSimulation")
set_vp_proxy(motion.Name, "CommandCreateSimulation", "ViewProviderMotion")
doc.recompute()

save(doc, OUT, hidden=(motion.Name,))
dump_mesh(doc, os.path.join(HERE, "preview", "dribox_large.json"))
