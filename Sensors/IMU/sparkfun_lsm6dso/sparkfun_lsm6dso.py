"""SparkFun 6DoF IMU Breakout - LSM6DSO (Qwiic).

1.0 x 1.0 in (25.4 x 25.4 mm) x 1.6 mm red PCB, 4 x 3.3 mm mounting holes
(0.1 in from edges), two Qwiic JST-SH 4-pin connectors on the left/right edges,
0.1 in PTH header row along the bottom edge.  Origin: centre of PCB underside,
Z up.  Sensor axes printed per datasheet: chip at board centre.
Run: freecad.cmd sparkfun_lsm6dso.py
"""
import os
import sys

sys.path.insert(0, "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
from fcutil import V, box, rbox_c, cyl, fuse, cut, compound, text, part, feat, save, dump_mesh, HERE

RED = (0.75, 0.08, 0.08)
SILK = (0.97, 0.97, 0.97)
GOLD = (0.85, 0.70, 0.30)
IC = (0.10, 0.10, 0.11)
JST = (0.92, 0.92, 0.90)
TIN = (0.8, 0.8, 0.82)

L, T, IN = 25.4, 1.6, 25.4
doc = App.newDocument("SparkFun_LSM6DSO")
p = part(doc, "LSM6DSO_Breakout", None, "SparkFun LSM6DSO Qwiic")
hc = L / 2 - 2.54
holes = [(x, y) for x in (-hc, hc) for y in (-hc, hc)]
pins = [(-6.35 + i * 2.54, -L / 2 + 1.9) for i in range(6)]

pcb = rbox_c(0, 0, 0, L, L, T, r=1.0)
pcb = cut(pcb, [cyl(1.65, 4, (x, y, -1)) for x, y in holes] + [cyl(0.5, 4, (x, y, -1)) for x, y in pins])
feat(doc, p, "PCB", pcb, RED, "PCB")
feat(doc, p, "Pads", compound(
    [cut(cyl(2.4, T + 0.06, (x, y, -0.03)), cyl(1.65, 4, (x, y, -1))) for x, y in holes] +
    [cut(cyl(0.85, T + 0.06, (x, y, -0.03)), cyl(0.5, 4, (x, y, -1))) for x, y in pins]), GOLD,
    "Plated holes")
Z = T

feat(doc, p, "LSM6DSO", box(-1.25, -1.5, Z, 2.5, 3.0, 0.86), IC, "LSM6DSO (LGA-14)")
feat(doc, p, "Pin1Dot", cyl(0.15, 0.02, (-0.9, 1.15, Z + 0.86)), SILK, "Pin-1 mark")


def qwiic(x, facing):
    """JST SM04B-SRSS-TB right-angle, opening toward facing (+1 = +X)."""
    w, d, h = 4.25, 6.0, 2.95
    body = box(x - w / 2, -d / 2, Z, w, d, h)
    mouth = box(x + (w / 2 - 3.0 + 0.01 if facing > 0 else -w / 2 - 0.01), -2.25, Z + 0.6, 3.0, 4.5, 1.7)
    tabs = [box(x - 0.6, y, Z, 1.2, 0.8, 1.0) for y in (-d / 2 - 0.8, d / 2)]
    return cut(body, mouth), compound(tabs)


for nm, x, f in (("QwiicL", -L / 2 + 2.3, -1), ("QwiicR", L / 2 - 2.3, 1)):
    b, t = qwiic(x, f)
    feat(doc, p, nm, b, JST, "Qwiic connector " + nm[-1])
    feat(doc, p, nm + "Tabs", t, TIN, "Qwiic tabs " + nm[-1])

feat(doc, p, "Caps", compound([box(x, y, Z, 1.0, 0.5, 0.5) for x, y in
                               ((2.4, 0.5), (2.4, -1.0), (-3.4, -1.0))]), (0.6, 0.5, 0.4), "Capacitors")
feat(doc, p, "Resistors", compound([box(x, y, Z, 1.0, 0.5, 0.35) for x, y in
                                    ((-3.0, 4.5), (-1.4, 4.5), (0.2, 4.5), (5.0, -5.5))]), IC, "Resistors")
feat(doc, p, "PowerLED", box(4.6, -7.0, Z, 1.0, 0.5, 0.4), (0.95, 0.1, 0.1), "Power LED")
feat(doc, p, "Jumpers", compound([box(x, 6.2, Z, 0.6, 1.0, 0.04) for x in (2.0, 2.8, 3.6)]), GOLD,
     "Solder jumpers")
feat(doc, p, "Silk", compound([
    text("LSM6DSO", 1.6, 0, 9.3, Z, 0.03),
    text("GND 3V3 SDA SCL INT1 INT2", 0.75, 0, -L / 2 + 3.6, Z, 0.03),
    text("x", 1.0, 5.6, 2.2, Z, 0.03), text("y", 1.0, 3.8, 4.4, Z, 0.03)]), SILK, "Silkscreen")
feat(doc, p, "AxisArrows", compound([box(3.8, 2.0, Z, 2.4, 0.2, 0.03), box(3.8, 2.0, Z, 0.2, 2.0, 0.03)]),
     SILK, "Axis marker")

doc.recompute()
save(doc, os.path.join(HERE, "sparkfun_lsm6dso.FCStd"))
dump_mesh(doc, os.path.join(HERE, "preview", "sparkfun_lsm6dso.json"), tol=0.05)
