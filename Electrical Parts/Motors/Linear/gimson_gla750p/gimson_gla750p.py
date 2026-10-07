"""Gimson Robotics GLA750-P 12 V DC linear actuator, 100 mm stroke, 240 mm installation length.

Run headless:  freecad.cmd gimson_gla750p.py   ->  gimson_gla750p.FCStd

The GLA750-P is no longer listed on gimsonrobotics.co.uk, so the form follows
Gimson's current parallel-motor actuators (GLA1500-N style): aluminium
extruded tube with the motor alongside it, cast gearbox housing at the rear with
the rear clevis lug, end cap and a stainless rod with a cross-drilled end.
Fixed by the brief: 100 mm stroke, 240 mm pin-to-pin when retracted; the
other dimensions are estimates for a 750 N class unit (20 mm rod, 32 mm motor,
6.2 mm pin holes).

Assembly: the body is grounded; the rod rides on a Slider joint along the
actuator axis.  Drag the rod, or run the "Extend and retract" simulation
(0 -> 100 mm -> 0).  Saved 40 mm extended.

Axes: X = actuator axis (rear pin at X=0, front pin at X=240 retracted),
pin holes along Y, motor above the tube (+Z).
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
from fcutil import (V, box, rbox_c, cyl, fuse, cut, compound, text, part, feat, save,
                    dump_mesh, set_vp_proxy, HERE)

OUT = os.path.join(HERE, "gimson_gla750p.FCStd")

ALU = (0.80, 0.81, 0.83)
CAST = (0.62, 0.63, 0.64)
BLACK = (0.08, 0.08, 0.09)
STEEL = (0.86, 0.86, 0.88)
WHITE = (0.95, 0.95, 0.95)
RED = (0.85, 0.12, 0.12)
CABLE = (0.10, 0.10, 0.10)

STROKE = 100.0
INSTALL = 240.0                 # pin-to-pin, retracted
PIN_D = 6.2
ROD_R = 10.0
MOTOR_R, MOTOR_Z = 16.0, 33.0
TUBE = (30.0, 30.0)             # extrusion section (Y, Z)
X_HOUSE = (10.0, 58.0)
X_TUBE = (58.0, 200.0)
X_CAP = (200.0, 210.0)
X_MOTOR = (58.0, 168.0)
X_ROD0 = 90.0                   # rod's rear end when retracted (inside the tube)
EXT = float(os.environ.get("GLA_EXT", "40"))   # saved extension, mm


def xbox(cy, cz, ly, lz, x0, length, r=0.0):
    """Rounded-rectangle prism along +X; section centred at (cy, cz)."""
    s = rbox_c(-cz, cy, x0, lz, ly, length, r=r)
    s.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    return s


def xcyl(r, x0, length, y=0.0, z=0.0):
    return cyl(r, length, (x0, y, z), (1, 0, 0))


def side_text(s, size, x, z, y_face, h=0.3):
    """Text on a -Y facing side, reading along +X."""
    t = text(s, size, x, 0, 0, h)
    t.rotate(V(0, 0, 0), V(1, 0, 0), 90)
    t.translate(V(0, y_face, z))
    return t


doc = App.newDocument("GLA750P")
asm = doc.addObject("Assembly::AssemblyObject", "Assembly")
asm.Label = "Gimson GLA750-P 100mm"
joints = asm.newObject("Assembly::JointGroup", "Joints")

# ======================================================================
# BODY
# ======================================================================
body = part(doc, "Body", asm, "Body")

hy, hz0, hz1 = 19.0, -17.0, MOTOR_Z + MOTOR_R + 1.5
housing = xbox(0, (hz0 + hz1) / 2, 2 * hy, hz1 - hz0, X_HOUSE[0], X_HOUSE[1] - X_HOUSE[0], r=5)
# rear clevis lug
lug = fuse([box(-1, -5, -8, X_HOUSE[0] + 4, 10, 16),
            cyl(8, 10, (0, -5, 0), (0, 1, 0))])
housing = fuse([housing, lug])
housing = cut(housing, cyl(PIN_D / 2, 30, (0, -15, 0), (0, 1, 0)))
# split line + screw heads on the housing sides
feat(doc, body, "Gearbox", housing, CAST, "Gearbox housing")
screws = [cyl(2.6, 1.0, (x, sy * hy, z), (0, sy, 0)) for sy in (-1, 1)
          for x, z in ((16, -11), (52, -11), (16, hz1 - 6), (52, hz1 - 6))]
seam = cut(xbox(0, (hz0 + hz1) / 2, 2 * hy + 0.4, hz1 - hz0 + 0.4, 33.8, 0.4, r=5.2),
           xbox(0, (hz0 + hz1) / 2, 2 * hy - 1, hz1 - hz0 - 1, 33, 2, r=4.5))
feat(doc, body, "GearboxScrews", compound(screws + [seam]), BLACK, "Housing screws / seam")

# extruded aluminium tube with side grooves
tube = xbox(0, 0, TUBE[0], TUBE[1], X_TUBE[0] - 1, X_TUBE[1] - X_TUBE[0] + 1, r=4)
tube = cut(tube, [xcyl(ROD_R + 1.0, X_TUBE[0] - 2, 200)]
           + [box(X_TUBE[0] + 2, sy * (TUBE[0] / 2) - 1.0, z - 1.2, X_TUBE[1] - X_TUBE[0] - 4,
                  2.0, 2.4) for sy in (-1, 1) for z in (-6, 6)])
feat(doc, body, "Tube", tube, ALU, "Outer tube (aluminium)")

# front end cap with screws, and internal drive nut (slider reference)
cap = xbox(0, 0, TUBE[0] + 2, TUBE[1] + 2, X_CAP[0], X_CAP[1] - X_CAP[0], r=5)
cap = cut(cap, xcyl(ROD_R + 0.3, X_CAP[0] - 1, 20))
feat(doc, body, "EndCap", cap, CAST, "End cap")
feat(doc, body, "EndCapScrews", compound([xcyl(1.6, X_CAP[1], 0.8, sy * 11.5, sz * 11.5)
                                          for sy in (-1, 1) for sz in (-1, 1)]), BLACK,
     "End cap screws")
nut = cut(xcyl(ROD_R + 0.9, X_ROD0 - 8, 8), xcyl(ROD_R, X_ROD0 - 9, 10))
nut_obj = feat(doc, body, "DriveNut", nut, BLACK, "Drive nut stop (slider reference)")

# motor alongside the tube
motor = xcyl(MOTOR_R, X_MOTOR[0] - 1, X_MOTOR[1] - X_MOTOR[0] + 1, z=MOTOR_Z)
feat(doc, body, "Motor", motor, ALU, "Motor can")
mcap = fuse([xcyl(MOTOR_R + 0.3, X_MOTOR[1], 7, z=MOTOR_Z),
             xcyl(6, X_MOTOR[1] + 7, 1.5, z=MOTOR_Z)])
feat(doc, body, "MotorCap", mcap, CAST, "Motor end cap")
feat(doc, body, "MotorCapScrews", compound([xcyl(1.4, X_MOTOR[1] + 7, 0.8, sy * 10, MOTOR_Z)
                                            for sy in (-1, 1)]), BLACK, "Motor cap screws")
# wrap-around label on the motor
lbl = cut(xcyl(MOTOR_R + 0.15, 72, 80, z=MOTOR_Z), xcyl(MOTOR_R + 0.01, 70, 84, z=MOTOR_Z))
lbl = lbl.common(box(70, -MOTOR_R - 2, MOTOR_Z - 6, 84, 2 * MOTOR_R + 4, MOTOR_R + 10))
red = cut(xcyl(MOTOR_R + 0.25, 92, 22, z=MOTOR_Z), xcyl(MOTOR_R + 0.1, 90, 26, z=MOTOR_Z))
red = red.common(box(90, -MOTOR_R - 2, MOTOR_Z + 6, 26, 2 * MOTOR_R + 4, MOTOR_R))
feat(doc, body, "Label", lbl, WHITE, "Label")
feat(doc, body, "LabelStripe", red, RED, "Label stripe")
feat(doc, body, "SideText", compound([
    side_text("GIMSON ROBOTICS", 3.2, 34, 22, -hy),
    side_text("GLA750-P 12V DC", 3.0, 34, 10, -hy)]), BLACK, "Housing text")

# cable gland + cable stub out of the back of the housing
gland = fuse([xcyl(5.5, X_HOUSE[0] - 4, 4, z=MOTOR_Z), xcyl(4.0, X_HOUSE[0] - 9, 5, z=MOTOR_Z)])
feat(doc, body, "CableGland", gland, BLACK, "Cable gland")
cable = Part.makeCylinder(2.5, 40, V(X_HOUSE[0] - 9, 0, MOTOR_Z), V(-1, 0, -0.6))
feat(doc, body, "Cable", cable, CABLE, "Cable (stub)")

# ======================================================================
# ROD (modelled retracted)
# ======================================================================
rod = part(doc, "Rod", asm, "Rod")
X_TIP = INSTALL + 8.0
rshape = xcyl(ROD_R, X_ROD0, X_TIP - X_ROD0)
rshape = cut(rshape, [cyl(PIN_D / 2, 30, (INSTALL, -15, 0), (0, 1, 0)),
                      # small chamfer-like groove near the tip
                      cut(xcyl(ROD_R + 1, X_TIP - 1.0, 2), xcyl(ROD_R - 0.6, X_TIP - 2, 4))])
rod_obj = feat(doc, rod, "RodTube", rshape, STEEL, "Rod (stainless)")

doc.recompute()

# ======================================================================
# JOINTS — slider along X
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

slider = joints.newObject("App::FeaturePython", "RodSlider")
JointObject.Joint(slider, JointObject.JointTypes.index("Slider"))
slider.Label = "Rod stroke (slider)"
set_vp_proxy(slider.Name, "JointObject", "ViewProviderJoint")

# the rod's rear end circle sits on the drive nut's front bore circle when retracted
ref = V(X_ROD0, 0, 0)
eb = circle_edge(nut_obj, ref, ROD_R)
er = circle_edge(rod_obj, ref, ROD_R)
slider.Proxy.setJointConnectors(slider, [
    [body, ["DriveNut." + eb, "DriveNut." + eb]],
    [rod, ["RodTube." + er, "RodTube." + er]],
])
doc.recompute()

rod.Placement = App.Placement(V(EXT, 0, 0), App.Rotation())
print("solve ->", asm.solve(), rod.Placement)

# ---- simulation: full stroke out and back, starting from the saved extension
# the motion value is the absolute slider travel in mm (0 = retracted, + = extending)
if not App.GuiUp:  # the module subclasses QtCore.QObject at import time
    builtins.QtCore = types.SimpleNamespace(QObject=object)
import UtilsAssembly
from CommandCreateSimulation import Simulation, Motion

half = STROKE / 2
phase = math.asin((EXT - half) / half)
sim = UtilsAssembly.getSimulationGroup(asm).newObject("App::FeaturePython", "RodSimulation")
Simulation(sim)
sim.Label = "Extend and retract"
sim.bTimeEnd = 6.0
sim.cTimeStepOutput = 0.04
motion = asm.newObject("App::FeaturePython", "RodMotion")
Motion(motion, "Linear", [slider, [""]],
       "%g+%g*sin(pi*time/3+%.6f)" % (half, half, phase))
motion.Label = "Rod travel"
sim.Group = [motion]
set_vp_proxy(sim.Name, "CommandCreateSimulation", "ViewProviderSimulation")
set_vp_proxy(motion.Name, "CommandCreateSimulation", "ViewProviderMotion")
doc.recompute()

save(doc, OUT, hidden=(motion.Name,))
dump_mesh(doc, os.path.join(HERE, "preview", "gimson_gla750p.json"))
