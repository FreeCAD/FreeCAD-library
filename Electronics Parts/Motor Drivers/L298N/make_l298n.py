# Parametric FreeCAD model of the common red L298N dual H-bridge motor driver module.
#
# Copyright (c) 2026. Licensed under Creative Commons Attribution 3.0 Unported
# (CC BY 3.0) - https://creativecommons.org/licenses/by/3.0/
#
# Run in the FreeCAD GUI (for colours):   freecad make_l298n.py
# or headless (no colours):               freecad.cmd make_l298n.py
#
# Outputs L298N.FCStd, L298N.step and L298N.stl next to this script.
# Coordinates: PCB lower-left corner at origin, PCB top face at z = 0 + PCB_T,
# "front" (power terminal + logic header) is the -Y edge.

import os
import FreeCAD as App
import Part
from FreeCAD import Vector as V

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- Dimensions (mm), typical values measured from the common module ----
PCB_W = 43.0
PCB_T = 1.6
HOLE_D = 3.2
HOLE_INSET = 3.0           # hole centre distance from PCB edge
TOP = PCB_T                # z of PCB top surface

HS_W, HS_D, HS_H = 23.0, 16.0, 25.0  # heatsink
HS_FINS = 7
HS_BASE_D = 3.0

TB_PITCH = 5.08            # screw terminal
TB_DEPTH = 7.6
TB_H = 10.0

HDR_PITCH = 2.54

BLUE, BLACK = (0.1, 0.35, 0.85), (0.08, 0.08, 0.08)
COLORS = {
    "pcb": (0.75, 0.05, 0.05),
    "heatsink": BLACK,
    "ic": (0.15, 0.15, 0.15),
    "metal": (0.8, 0.8, 0.82),
    "gold": (0.85, 0.7, 0.2),
    "terminal": BLUE,
    "plastic": BLACK,
    "jumper": BLACK,
    "cap": (0.1, 0.1, 0.12),
    "led": (0.9, 0.1, 0.1),
    "smd": (0.2, 0.2, 0.2),
}

doc = App.newDocument("L298N")
doc.Meta = dict(doc.Meta, License="CC BY 3.0")
doc.License = "Creative Commons Attribution 3.0 Unported (CC BY 3.0)"
doc.LicenseURL = "https://creativecommons.org/licenses/by/3.0/"
doc.Comment = "L298N dual H-bridge motor driver module, simplified 3D model"

parts = []  # (name, shape, colour key)


def add(name, shape, color):
    parts.append((name, shape, color))


def box(x, y, z, w, d, h):
    return Part.makeBox(w, d, h, V(x, y, z))


def cyl(x, y, z, r, h, axis=V(0, 0, 1)):
    return Part.makeCylinder(r, h, V(x, y, z), axis)


# ---- PCB with mounting holes ----
pcb = box(0, 0, 0, PCB_W, PCB_W, PCB_T)
for hx in (HOLE_INSET, PCB_W - HOLE_INSET):
    for hy in (HOLE_INSET, PCB_W - HOLE_INSET):
        pcb = pcb.cut(cyl(hx, hy, -1, HOLE_D / 2, PCB_T + 2))
add("PCB", pcb, "pcb")

# ---- Heatsink (finned, at the back) with L298N Multiwatt15 in front of it ----
hs_x = (PCB_W - HS_W) / 2
hs_y = PCB_W - HS_D - 4.0
heatsink = box(hs_x, hs_y, TOP, HS_W, HS_BASE_D, HS_H)
fin_t = 1.4
fin_gap = (HS_W - fin_t) / (HS_FINS - 1)
for i in range(HS_FINS):
    heatsink = heatsink.fuse(box(hs_x + i * fin_gap, hs_y, TOP, fin_t, HS_D, HS_H))
heatsink = heatsink.fuse(box(hs_x, hs_y, TOP, HS_W, HS_D, 2.0))  # bottom web
heatsink = heatsink.removeSplitter()
add("Heatsink", heatsink, "heatsink")

# IC body: 20 x 5 x 10.7 mm, mounted vertically against heatsink front face
ic_w, ic_t, ic_h = 20.0, 5.0, 10.7
ic_x = (PCB_W - ic_w) / 2
ic_y = hs_y - ic_t
ic_z = TOP + 5.0
ic = box(ic_x, ic_y, ic_z, ic_w, ic_t, ic_h)
tab = box(ic_x, hs_y - 1.6, ic_z + ic_h, ic_w, 1.6, 6.5)  # metal tab
tab = tab.cut(cyl(PCB_W / 2, hs_y - 2, ic_z + ic_h + 3.5, 1.6, 4, V(0, 1, 0)))
add("L298N", ic, "ic")
add("L298N_tab", tab, "metal")
# Multiwatt15 leads: 15 pins, 1.27 mm pitch, staggered into two rows
leads = None
for i in range(15):
    lx = PCB_W / 2 + (i - 7) * 1.27 - 0.25
    ly = ic_y + (0.5 if i % 2 else 2.5)
    lead = box(lx, ly, TOP - PCB_T, 0.5, 0.4, ic_z - TOP + PCB_T + 0.1)
    leads = lead if leads is None else leads.fuse(lead)
add("L298N_leads", leads, "metal")
# Heatsink screw
add("Heatsink_screw", cyl(PCB_W / 2, hs_y - 1.6, ic_z + ic_h + 3.5, 2.6, 1.6, V(0, -1, 0)), "metal")


# ---- Screw terminals ----
def terminal(name, n, x, y, rot):
    """n-way 5.08 mm terminal block; rot=0 wires enter from -Y, 90 from -X, -90 from +X."""
    L = n * TB_PITCH
    body = box(0, 0, 0, L, TB_DEPTH, TB_H)
    screws = None
    for i in range(n):
        cx = TB_PITCH / 2 + i * TB_PITCH
        body = body.cut(box(cx - 1.75, -0.1, 1.5, 3.5, 4.5, 3.5))   # wire entry
        body = body.cut(cyl(cx, 4.6, TB_H - 3, 1.5, 3.1))           # screw well
        s = cyl(cx, 4.6, TB_H - 3.5, 1.4, 3.0).cut(box(cx - 1.4, 4.4, TB_H - 1, 2.8, 0.4, 1))
        screws = s if screws is None else screws.fuse(s)
    pl = App.Placement(V(x, y, TOP), App.Rotation(V(0, 0, 1), rot))
    body.Placement = pl
    screws.Placement = pl
    add(name, body, "terminal")
    add(name + "_screws", screws, "metal")


# 3-pin power (+12V, GND, +5V) front-left, wires from front
terminal("TB_Power", 3, 3.5, 0.5, 0)
# OUT1/OUT2 on the left edge, OUT3/OUT4 on the right edge
terminal("TB_OUT1_OUT2", 2, 0.5, 13.0 + 2 * TB_PITCH, -90)
terminal("TB_OUT3_OUT4", 2, PCB_W - 0.5, 13.0, 90)


# ---- Pin headers ----
def header(name, n, x, y, jumpers=()):
    base = None
    pins = None
    for i in range(n):
        px = x + i * HDR_PITCH
        b = box(px - 1.27, y - 1.27, TOP, 2.54, 2.54, 2.5)
        p = box(px - 0.32, y - 0.32, TOP - 3.0, 0.64, 0.64, 11.5 + 3.0)
        base = b if base is None else base.fuse(b)
        pins = p if pins is None else pins.fuse(p)
    add(name + "_base", base.removeSplitter(), "plastic")
    add(name + "_pins", pins, "gold")
    for j in jumpers:  # jumper shunt bridging pins j and j+1
        jx = x + j * HDR_PITCH - 1.27
        sh = box(jx, y - 1.27, TOP + 2.5, 2 * HDR_PITCH, 2.54, 6.0)
        add("%s_jumper%d" % (name, j), sh, "jumper")


# 6-pin logic header ENA IN1 IN2 IN3 IN4 ENB (front-right), ENA/ENB each
# jumpered to a 5 V pin behind them -> modelled as a 2-row header at the ends
hdr_y = 4.0
hdr_x = 22.0
header("Header_Logic", 6, hdr_x, hdr_y)
header("Header_ENA_5V", 1, hdr_x, hdr_y + HDR_PITCH)
header("Header_ENB_5V", 1, hdr_x + 5 * HDR_PITCH, hdr_y + HDR_PITCH)
for k, jx in enumerate((hdr_x, hdr_x + 5 * HDR_PITCH)):
    add("Jumper_EN%s" % "AB"[k],
        box(jx - 1.27, hdr_y - 1.27, TOP + 2.5, 2.54, 2 * HDR_PITCH, 6.0), "jumper")
# 5 V regulator enable jumper (behind power terminal)
header("Header_5V_EN", 2, 3.0, 10.5, jumpers=(0,))


# ---- Electrolytic capacitors (220 uF, 8 x 11 mm) ----
def ecap(name, x, y, d=8.0, h=11.0):
    body = cyl(x, y, TOP + 0.3, d / 2, h - 0.3)
    body = body.cut(cyl(x, y, TOP + h - 0.3, d / 2 - 0.6, 0.4))  # top recess
    add(name, body, "cap")
    add(name + "_top", cyl(x, y, TOP + h - 0.3, d / 2 - 0.6, 0.1), "metal")


ecap("C_220uF_1", 13.0, 13.5)
ecap("C_220uF_2", 30.0, 13.5)

# ---- 78M05 regulator (DPAK / TO-252) ----
reg = box(18.0, 10.0, TOP, 6.6, 6.1, 2.3)
add("U_78M05", reg, "ic")
add("U_78M05_tab", box(18.6, 16.1, TOP, 5.4, 1.2, 0.5), "metal")
for lx in (18.9, 23.0):
    add("U_78M05_lead_%g" % lx, box(lx, 8.6, TOP, 0.8, 1.4, 0.5), "metal")

# ---- Small SMD parts: 8 flyback diodes (M7 / SMA), LED, resistors ----
for i in range(4):
    for side, dx in (("L", 3.0), ("R", 35.7)):
        x = dx
        y = 25.0 + i * 3.2
        add("D_%s%d" % (side, i + 1), box(x, y, TOP, 4.3, 2.6, 2.0), "smd")
        add("D_%s%d_band" % (side, i + 1), box(x + 0.4, y - 0.01, TOP + 0.01, 0.6, 2.62, 2.0), "metal")
add("LED_Power", box(36.0, 9.0, TOP, 1.6, 0.8, 0.8), "led")
for i, (x, y) in enumerate([(36.0, 11.0), (38.5, 9.0), (38.5, 11.0)]):
    add("R%d" % (i + 1), box(x, y, TOP, 1.6, 0.8, 0.5), "smd")
add("C_100nF", box(25.5, 8.3, TOP, 2.0, 1.25, 0.9), "smd")

# ---- Build document ----
objs = []
for name, shape, col in parts:
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    objs.append((o, col))
doc.recompute()

if App.GuiUp:
    for o, col in objs:
        o.ViewObject.ShapeColor = COLORS[col]

grp = doc.addObject("App::Part", "L298N_Module")
for o, _ in objs:
    grp.addObject(o)
grp.Label2 = "CC BY 3.0"
doc.recompute()

doc.saveAs(os.path.join(OUT_DIR, "L298N.FCStd"))

import Import, Mesh
Import.export([grp], os.path.join(OUT_DIR, "L298N.step"))
Mesh.export([o for o, _ in objs], os.path.join(OUT_DIR, "L298N.stl"))
App.Console.PrintMessage("L298N model written to %s\n" % OUT_DIR)

if App.GuiUp:
    import FreeCADGui as Gui
    Gui.activeDocument().activeView().viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().saveImage(os.path.join(OUT_DIR, "L298N.png"), 1200, 900, "White")
    doc.save()
    if os.environ.get("L298N_QUIT"):
        Gui.getMainWindow().close()
