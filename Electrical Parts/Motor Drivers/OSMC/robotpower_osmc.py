"""Robot Power OSMC (Open Source Motor Controller) rev 3-2 H-bridge power board.

Run headless:  freecad.cmd robotpower_osmc.py   ->  robotpower_osmc.FCStd

Board outline, mounting / fan holes, bolt pads and the main part positions
come from Robot Power's published OSMC3-2 gerbers + drill file
(robotpower.com/downloads/osmc3-2-08222001-gerbers.zip); part bodies are
standard package sizes, arranged as in the product photos:
  - 16 x IRFB3207 TO-220 MOSFETs standing in two banks of 8
  - 2 large bus electrolytics between the banks
  - HIP4081A DIP-20 bridge driver, 10-pin shrouded logic header,
    2-pin fan/12V screw terminal, power LED
  - four #8-bolt power pads (B+, GND, MOT+, MOT-)
  - 80 mm cooling fan on 4 standoffs over the MOSFETs (Fan* objects; hide them
    for the bare board), plus 4 corner mounting standoffs underneath

Axes: X along the 4.40" edge, Y along the 3.15" edge, Z up; origin at the
board's lower-left corner, PCB underside at Z=0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
import Part
from fcutil import (V, box, rbox, rbox_c, cyl, fuse, cut, compound, text, part, feat, save,
                    dump_mesh, HERE)

OUT = os.path.join(HERE, "robotpower_osmc.FCStd")

GREEN = (0.05, 0.38, 0.16)
BLACK = (0.06, 0.06, 0.07)
TAB = (0.78, 0.79, 0.81)
TIN = (0.80, 0.80, 0.82)
ALU = (0.80, 0.81, 0.83)
GREY = (0.55, 0.56, 0.58)
CAPC = (0.10, 0.10, 0.12)
WHITE = (0.92, 0.92, 0.92)
RED = (0.85, 0.10, 0.08)
REDCAP = (0.80, 0.25, 0.15)
TERM = (0.25, 0.80, 0.40)
FANC = (0.12, 0.12, 0.13)

IN = 25.4
X0, Y0 = 4.30, 4.75            # gerber coordinates (inch) of the board corner
BW, BH = 4.40 * IN, 3.15 * IN  # 111.8 x 80.0 mm
T = 1.6
ZT = T                          # top copper


def P(x, y):
    """Gerber inch coordinates -> model mm."""
    return ((x - X0) * IN, (y - Y0) * IN)


doc = App.newDocument("OSMC")
osmc = part(doc, "OSMC", None, "Robot Power OSMC 3-2")

# ---- PCB with holes (from the drill file)
MOUNT = [(4.45, 7.70), (4.45, 4.95), (5.7425, 7.7326), (5.743, 4.918), (8.5574, 7.7325),
         (8.5575, 4.9175)]                                   # 0.187" holes
BOLT = {"B+": (6.70, 7.525), "MOT-": (7.325, 7.325), "GND": (6.80, 5.45),
        "MOT+": (7.45, 5.375)}                               # 0.136" #8-bolt pads
pcb = box(0, 0, 0, BW, BH, T)
pcb = cut(pcb, [cyl(0.187 * IN / 2, 4, P(*h) + (-1,)) for h in MOUNT]
          + [cyl(0.136 * IN / 2, 4, P(*h) + (-1,)) for h in BOLT.values()])
feat(doc, osmc, "PCB", pcb, GREEN, "PCB")

# bolt pads: tinned rings top and bottom
pads = []
for x, y in BOLT.values():
    px, py = P(x, y)
    for z in (ZT, -0.1):
        pads.append(cut(cyl(5.2, 0.1, (px, py, z)), cyl(1.8, 1, (px, py, z - 0.5))))
for x, y in MOUNT:
    px, py = P(x, y)
    pads.append(cut(cyl(3.6, 0.05, (px, py, ZT)), cyl(2.5, 1, (px, py, ZT - 0.5))))
feat(doc, osmc, "Pads", compound(pads), TIN, "Bolt + mounting pads")

# ---- MOSFETs: TO-220 standing upright in two banks (fan blows down between them)
LEFT_Y = [7.62, 7.36, 7.10, 6.84, 6.27, 6.01, 5.75, 5.49]
RIGHT_Y = [7.60, 7.34, 7.06, 6.80, 6.22, 5.94, 5.66, 5.38]


def to220(cx, cy):
    """Upright TO-220 centred at (cx, cy): leads in a row along X, metal tab on the -Y face."""
    leads = []
    zb = ZT + 3.0
    body = box(cx - 5.0, cy - 2.25, zb, 10.0, 4.5, 9.15)
    tab = box(cx - 5.0, cy - 2.25, zb, 10.0, 1.3, 15.6)
    tab = cut(tab, cyl(1.8, 4, (cx, cy - 3, zb + 12.8), (0, 1, 0)))
    for k in (-2.54, 0, 2.54):
        leads.append(box(cx + k - 0.4, cy - 0.25, ZT, 0.8, 0.5, 3.1))
    return body, tab, leads


mb, mt, ml = [], [], []
for xs, ys in ((6.12, LEFT_Y), (7.88, RIGHT_Y)):
    for y in ys:
        px, py = P(xs, y)
        b, t_, l = to220(px, py)
        mb.append(b)
        mt.append(t_)
        ml += l
feat(doc, osmc, "MOSFETs", compound(mb), BLACK, "MOSFETs IRFB3207 x16")
feat(doc, osmc, "MOSFETTabs", compound(mt), TAB, "MOSFET tabs")
feat(doc, osmc, "MOSFETLeads", compound(ml), TIN, "MOSFET leads")

# ---- bus capacitors (radial electrolytic, 16 x 26 mm) with sleeve marking
caps, capt = [], []
for x, y in ((6.95, 6.92), (6.95, 6.17)):
    px, py = P(x, y)
    caps.append(cyl(8.0, 25.5, (px, py, ZT + 0.5)))
    capt.append(cut(cyl(7.2, 0.3, (px, py, ZT + 26.0)), cyl(2.0, 1, (px, py, ZT + 25.5))))
    capt.append(box(px + 7.85, py - 2.2, ZT + 1.0, 0.3, 4.4, 24.0))  # minus stripe
feat(doc, osmc, "BusCaps", compound(caps), CAPC, "Bus capacitors")
feat(doc, osmc, "BusCapTops", compound(capt), ALU, "Capacitor tops / stripe")

# ---- driver, logic header, terminal, LED, small parts
dx, dy = P(5.44, 6.05)
feat(doc, osmc, "Driver", rbox_c(dx, dy, ZT + 0.6, 7.0, 26.0, 3.3, r=0.3), BLACK,
     "HIP4081A driver (DIP-20)")
dpins = [box(dx + s * 3.6 - 0.25, dy - 11.43 + i * 2.54 - 0.25, ZT, 0.5, 0.5, 2.5)
         for s in (-1, 1) for i in range(10)]
feat(doc, osmc, "DriverPins", compound(dpins), TIN, "Driver pins")

hx, hy = P(4.60, 5.95)
hdr = rbox_c(hx, hy, ZT, 8.9, 20.4, 9.0, r=0.5)
hdr = cut(hdr, [rbox_c(hx, hy, ZT + 2.0, 6.3, 12.7 + 2.0, 8, r=0.3),
                box(hx - 5, hy - 2.25, ZT + 4.5, 2, 4.5, 6)])        # key slot
feat(doc, osmc, "LogicHeader", hdr, GREY, "Logic header 2x5 (shrouded)")
feat(doc, osmc, "HeaderPins", compound([box(hx + s * 1.27 - 0.32, hy - 5.08 + i * 2.54 - 0.32,
                                            ZT, 0.64, 0.64, 8.0)
                                        for s in (-1, 1) for i in range(5)]),
     (0.85, 0.70, 0.30), "Header pins")

tx, ty = P(4.65, 7.275)
term = rbox_c(tx, ty, ZT, 10.2, 7.6, 10.0, r=0.4)
term = cut(term, [cyl(1.4, 4, (tx + s * 2.54, ty, ZT + 7)) for s in (-1, 1)]
           + [box(tx + s * 2.54 - 1.8, ty - 4.5, ZT + 1.5, 3.6, 3.0, 3.6) for s in (-1, 1)])
feat(doc, osmc, "FanTerminal", term, TERM, "Fan / 12V terminal")
feat(doc, osmc, "TerminalScrews", compound([cyl(1.3, 0.6, (tx + s * 2.54, ty, ZT + 9.6))
                                            for s in (-1, 1)]), TIN, "Terminal screws")

lx, ly = P(4.62, 7.62)
feat(doc, osmc, "PowerLED", fuse([cyl(1.5, 3.5, (lx, ly, ZT + 1)), cyl(1.6, 1, (lx, ly, ZT + 1)),
                                  Part.makeSphere(1.5, V(lx, ly, ZT + 4.5))]), RED, "Power LED")

# 12 V regulator (DIP-8) + its parts near the top-left
rx, ry = P(5.15, 7.25)
feat(doc, osmc, "Regulator", rbox_c(rx, ry, ZT + 0.6, 9.6, 6.4, 3.3, r=0.3), BLACK,
     "12V regulator (DIP-8)")
small = []
for x, y, l, w in ((5.0, 6.95, 4.0, 1.6), (5.3, 6.95, 4.0, 1.6), (4.9, 6.5, 3.2, 1.6),
                   (5.65, 5.25, 3.2, 1.6), (5.9, 5.0, 3.2, 1.6), (6.6, 7.75, 3.2, 1.6),
                   (8.15, 7.0, 1.6, 3.2), (8.15, 6.55, 1.6, 3.2), (8.15, 5.95, 1.6, 3.2),
                   (8.15, 5.5, 1.6, 3.2), (6.55, 5.85, 3.2, 1.6), (7.2, 6.55, 3.2, 1.6)):
    px, py = P(x, y)
    small.append(rbox_c(px, py, ZT, l, w, 1.0, r=0.2))
feat(doc, osmc, "SMDParts", compound(small), (0.25, 0.22, 0.18), "Resistors / diodes")
gx, gy = P(7.05, 7.62)
feat(doc, osmc, "FastDiode", cyl(1.4, 5.2, (gx - 2.6, gy, ZT + 1.6), (1, 0, 0)),
     (0.15, 0.15, 0.18), "Bootstrap diode")
fc = []
for x, y in ((8.42, 6.45), (8.42, 6.10)):
    px, py = P(x, y)
    fc.append(rbox_c(px, py, ZT, 7.2, 4.0, 9.0, r=0.6, r_top=0.6))
feat(doc, osmc, "FilmCaps", compound(fc), REDCAP, "Film capacitors")

# ---- silkscreen
silk = [text("OSMC3-2", 2.4, *P(4.95, 5.28), ZT, 0.05),
        text("08/22/2001", 2.0, *P(4.95, 5.12), ZT, 0.05),
        text("PWR", 1.8, *P(4.62, 7.80), ZT, 0.05),
        text("GND +12V", 1.6, *P(5.05, 7.62), ZT, 0.05)]
for name, (x, y) in BOLT.items():
    px, py = P(x, y)
    silk.append(text(name, 2.2, px, py - 7.5 if y < 6 else py + 7.0, ZT, 0.05))
feat(doc, osmc, "Silkscreen", compound([s for s in silk if s]), WHITE, "Silkscreen")

# ---- mounting standoffs (underneath, corners)
def hexbar(cx, cy, z0, h, af=6.35):
    r = af / math.sqrt(3)
    poly = Part.makePolygon([V(cx + r * math.cos(a * math.pi / 3), cy + r * math.sin(a * math.pi / 3),
                               z0) for a in range(7)])
    return Part.Face(poly).extrude(V(0, 0, h))


corner = [MOUNT[0], MOUNT[1], MOUNT[4], MOUNT[5]]
feat(doc, osmc, "Standoffs", compound([hexbar(*P(*h), -12.0, 12.0) for h in corner]), ALU,
     "Mounting standoffs (below)")

# ---- 80 mm fan on standoffs over the MOSFETs
FAN_HOLES = [MOUNT[2], MOUNT[3], MOUNT[4], MOUNT[5]]
fcx = sum(P(*h)[0] for h in FAN_HOLES) / 4
fcy = sum(P(*h)[1] for h in FAN_HOLES) / 4
FZ = ZT + 30.0
feat(doc, osmc, "FanStandoffs", compound([hexbar(*P(*h), ZT, FZ - ZT) for h in FAN_HOLES]),
     ALU, "Fan standoffs")
frame = rbox_c(fcx, fcy, FZ, 80, 80, 25, r=4)
frame = cut(frame, [cyl(38.5, 30, (fcx, fcy, FZ - 1))]
            + [cyl(2.2, 30, (fcx + sx * 35.75, fcy + sy * 35.75, FZ - 1))
               for sx in (-1, 1) for sy in (-1, 1)]
            # corner recesses between the top and bottom mounting flanges
            + [rbox_c(fcx + sx * 33, fcy + sy * 33, FZ + 4, 14, 14, 17, r=2)
               for sx in (-1, 1) for sy in (-1, 1)])
frame = fuse([frame] + [cyl(3.0, 25, (fcx + sx * 35.75, fcy + sy * 35.75, FZ)).cut(
    cyl(2.2, 27, (fcx + sx * 35.75, fcy + sy * 35.75, FZ - 1))) for sx in (-1, 1) for sy in (-1, 1)])
feat(doc, osmc, "FanFrame", frame, FANC, "Fan frame (80 mm)")
hub = cyl(17, 22, (fcx, fcy, FZ + 1.5))
blades = []
for i in range(7):
    bl = box(fcx + 15, fcy - 1.0, FZ + 3, 22.5, 2.0, 18)
    bl.rotate(V(fcx + 26, fcy, FZ + 12), V(1, 0, 0), 35)
    bl.rotate(V(fcx, fcy, 0), V(0, 0, 1), i * 360 / 7)
    blades.append(bl)
feat(doc, osmc, "FanRotor", fuse([hub] + blades), (0.18, 0.18, 0.19), "Fan rotor")
spokes = [box(fcx, fcy - 1.0, FZ, 39, 2.0, 2.0).rotated(V(fcx, fcy, FZ), V(0, 0, 1), a)
          for a in (45, 135, 225, 315)]
feat(doc, osmc, "FanStruts", compound(spokes + [cyl(17, 2.0, (fcx, fcy, FZ))]), FANC,
     "Fan motor struts")

doc.recompute()
save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "robotpower_osmc.json"))
if os.environ.get("OSMC_PREVIEW_NOFAN"):
    dump_mesh(doc, os.path.join(HERE, "preview", "robotpower_osmc_nofan.json"),
              hidden=[o.Name for o in doc.Objects if o.Name.startswith("Fan")])
