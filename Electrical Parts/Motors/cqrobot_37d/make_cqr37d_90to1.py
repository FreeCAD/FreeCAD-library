# Parametric FreeCAD model: CQRobot 90:1 Metal DC Gearmotor 37Dx70.1L mm 6V/12V, 64 CPR encoder
# Licence: CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/)
# Approximate model. Dimensions not published by CQRobot follow the common 37D gearmotor pattern;
# verify against your part before using for tight-tolerance work.
# Run: freecad.cmd make_cqr37d_90to1.py   (or paste into the FreeCAD Python console)
import FreeCAD as App, Part
from FreeCAD import Vector as V
import math, os

# ---- parameters (mm) ----
GB_D, GB_L = 37.0, 26.5        # gearbox diameter / length (90:1)
MOT_D, MOT_L = 34.6, 33.6      # motor can
ENC_D, ENC_L = 34.6, 10.0      # encoder cap (GB_L+MOT_L+ENC_L = 70.1)
SHAFT_OFF = 7.0                # output shaft offset from body axis
BOSS_D, BOSS_L = 12.0, 6.0     # bearing boss on gearbox face
SH_D, SH_L, SH_FLAT = 6.0, 16.0, 0.5   # D-shaft dia, length beyond boss, flat depth
SH_FLAT_L = 15.0
HOLE_N, HOLE_PCD, HOLE_D, HOLE_DEPTH = 6, 31.0, 2.5, 3.0  # M3 tap-drill holes
WIRE_D, WIRE_L, WIRE_N = 1.6, 20.0, 6
BR_W, BR_H, BR_D, BR_T = 38.0, 30.0, 30.0, 3.0  # bracket width / face height / base depth / thickness
BR_AXIS_H = BR_T + GB_D/2 + 0.5                 # motor axis height above bracket underside
BR_SLOT_W, BR_SLOT_L = 3.4, 8.0                  # M3 slots in bracket base
FN = os.environ.get("CQR_OUT", os.path.join(os.getcwd(), "CQRobot_37D_90to1_64CPR"))

doc = App.newDocument("CQRobot_37D_90to1_64CPR")
z = 0.0  # +Z = output shaft direction; z=0 is gearbox front face

# gearbox with mounting holes
gb = Part.makeCylinder(GB_D/2, GB_L, V(0, 0, -GB_L))
for i in range(HOLE_N):
    a = math.radians(i*360/HOLE_N)
    gb = gb.cut(Part.makeCylinder(HOLE_D/2, HOLE_DEPTH, V(HOLE_PCD/2*math.cos(a), HOLE_PCD/2*math.sin(a), -HOLE_DEPTH)))
gb = gb.cut(Part.makeTorus(GB_D/2, 0.4, V(0, 0, -GB_L+3)))  # cosmetic groove

boss = Part.makeCylinder(BOSS_D/2, BOSS_L, V(0, -SHAFT_OFF, 0))

shaft = Part.makeCylinder(SH_D/2, SH_L, V(0, -SHAFT_OFF, BOSS_L))
flat = Part.makeBox(SH_D, SH_D, SH_FLAT_L, V(SH_D/2 - SH_FLAT, -SHAFT_OFF - SH_D/2, BOSS_L + SH_L - SH_FLAT_L))
shaft = shaft.cut(flat)

motor = Part.makeCylinder(MOT_D/2, MOT_L, V(0, 0, -GB_L - MOT_L))
enc = Part.makeCylinder(ENC_D/2, ENC_L, V(0, 0, -GB_L - MOT_L - ENC_L))
enc = enc.cut(Part.makeCylinder(ENC_D/2 - 1.5, 1.0, V(0, 0, -GB_L - MOT_L - ENC_L)))  # recessed back

wires = []
for i in range(WIRE_N):
    x = (i - (WIRE_N-1)/2) * (WIRE_D + 0.1)
    wires.append(Part.makeCylinder(WIRE_D/2, WIRE_L, V(x, -ENC_D/2 + 4, -GB_L - MOT_L - ENC_L), V(0, 0, -1)))

# L-bracket: face plate on gearbox front (z 0..BR_T), base under the motor running back along -Z
yb = -BR_AXIS_H  # bracket underside
face = Part.makeBox(BR_W, BR_H, BR_T, V(-BR_W/2, yb, 0))
base = Part.makeBox(BR_W, BR_T, BR_D, V(-BR_W/2, yb, BR_T - BR_D))
br = face.fuse(base).removeSplitter()
br = br.cut(Part.makeCylinder(BOSS_D/2 + 0.5, BR_T, V(0, -SHAFT_OFF, 0)))
for i in range(HOLE_N):
    a = math.radians(i*360/HOLE_N)
    x, y = HOLE_PCD/2*math.cos(a), HOLE_PCD/2*math.sin(a)
    if y - 1.7 > yb + BR_T and y + 1.7 < yb + BR_H:  # only holes that land on the face plate
        br = br.cut(Part.makeCylinder(1.7, BR_T, V(x, y, 0)))
for x in (-BR_W/4 - 2, BR_W/4 + 2):
    zc = BR_T - BR_D/2 - 2
    slot = Part.makeBox(BR_SLOT_W, BR_T, BR_SLOT_L - BR_SLOT_W, V(x - BR_SLOT_W/2, yb, zc - (BR_SLOT_L - BR_SLOT_W)/2))
    for dz in (-(BR_SLOT_L - BR_SLOT_W)/2, (BR_SLOT_L - BR_SLOT_W)/2):
        slot = slot.fuse(Part.makeCylinder(BR_SLOT_W/2, BR_T, V(x, yb, zc + dz), V(0, 1, 0)))
    br = br.cut(slot)

parts = [("Bracket", br, (0.3, 0.3, 0.32)), ("Gearbox", gb, (0.75, 0.75, 0.78)), ("Boss", boss, (0.8, 0.8, 0.8)),
         ("Shaft", shaft, (0.85, 0.85, 0.9)), ("Motor", motor, (0.6, 0.6, 0.62)),
         ("Encoder", enc, (0.1, 0.1, 0.1))]
cols = [(1,0,0),(0,0,0),(0,0.6,0),(0,0,1),(1,1,0),(1,1,1)]
for i, w in enumerate(wires):
    parts.append((f"Wire{i+1}", w, cols[i]))

objs = []
for name, shp, c in parts:
    o = doc.addObject("Part::Feature", name); o.Shape = shp
    if hasattr(o, "ViewObject") and o.ViewObject: o.ViewObject.ShapeColor = c
    objs.append(o)
doc.recompute()
doc.saveAs(FN + ".FCStd")
Part.export(objs, FN + ".step")
import Mesh; Mesh.export(objs, FN + ".stl")
bb = Part.makeCompound([o.Shape for o in objs[:6]]).BoundBox
print("Motor+bracket bbox:", bb)
for o in objs[:6]: print(o.Name, "valid" if o.Shape.isValid() else "INVALID", round(o.Shape.Volume,1))
print("Saved", FN)
