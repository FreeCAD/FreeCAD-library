# FreeCAD model of the Arduino GIGA R1 WiFi (ABX00063).
#
# Copyright (c) 2026. Licensed under Creative Commons Attribution 3.0 Unported
# (CC BY 3.0) https://creativecommons.org/licenses/by/3.0/
#
# Original work: geometry was drawn from scratch from published dimensions
# (ABX00063 datasheet sec. 15 "Mounting Holes And Board Outline" and the
# sec. 6.1 top-view placement drawing, on the standard Arduino Mega 0.1" grid).
# It is NOT derived from Arduino's CC BY-SA 4.0 STEP/CAD files.
# "Arduino" and "GIGA" are trademarks of Arduino S.r.l.; no logos are modelled.
#
# Exact: board outline, all mounting/locating holes, header positions.
# Estimated: component bodies (sizes from part datasheets, placement from the
# topology drawing), header heights, PCB colour.
#
# Run:  freecad arduino_giga_r1_wifi.py   (GUI: keeps colours, saves preview PNG)
#       freecad.cmd arduino_giga_r1_wifi.py (headless: geometry only)
# Writes arduino_giga_r1_wifi.FCStd and .step next to this script.

import os
import FreeCAD as App
import Part

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
NAME = "arduino_giga_r1_wifi"

# ---- Parameters (mm) ------------------------------------------------------
# Origin: bottom-left corner of the board (USB/audio edge at x=0, analog
# header edge at y=0), PCB bottom at z=0.
PCB_T = 1.6
P = 2.54                                  # header pitch
FH_H, FH_W = 8.5, 2.54                    # female header body height / width
PIN_W, TAIL = 0.64, 3.0                   # square pin, tail below PCB

# Datasheet outline: 101.60 x 53.34, 99.06 main edge, 32.77 / 37.55 nose.
OUTLINE = [(0, 0), (99.06, 0), (99.06, 2.54), (101.6, 4.93), (101.6, 37.70),
           (99.06, 40.09), (99.06, 51.82), (97.54, 53.34), (0, 53.34)]

HOLES = [  # (x, y, diameter)
    (15.24, 50.80, 3.2), (90.17, 50.80, 3.2), (66.04, 35.56, 3.2),
    (66.04, 7.62, 3.2), (13.97, 2.54, 3.2), (96.52, 2.54, 3.2),
    (20.07, 36.83, 1.8), (20.07, 16.51, 1.8),    # J6 header locating pegs
    (82.55, 39.37, 1.8), (82.55, 13.97, 1.8),    # J5 header locating pegs
    (7.92, 30.23, 2.3), (7.92, 17.02, 2.3),      # USB-A shell legs
    (4.70, 10.29, 1.7), (11.68, 10.29, 1.7),     # audio jack pegs
]

# Female headers: (name, x of first pin, y of first pin, cols, rows) — pins run
# +X along cols, +Y along rows. Positions in inches on the Mega grid.
IN = 25.4
FEMALE = [
    ("JDIGITAL_A", 0.74, 2.0, 10, 1),   # SCL1..D8
    ("JDIGITAL_B", 1.80, 2.0, 8, 1),    # D7..D0
    ("JDIGITAL_C", 2.70, 2.0, 8, 1),    # D14..D21
    ("JRTC",       0.70, 0.1, 3, 1),    # OFF / GND / VRTC
    ("JPOWER",     1.10, 0.1, 8, 1),    # NC IOREF RESET 3V3 5V GND GND VIN
    ("JANALOG_A",  2.00, 0.1, 8, 1),    # A0..A7
    ("JANALOG_B",  2.90, 0.1, 8, 1),    # A8..A11 DAC0 DAC1 CANRX CANTX
    ("JSIDE",      3.70, 0.3, 2, 18),   # 5V, D22..D53, GND
]
# SMD 2x10 female headers (camera J6, display J5): (name, x centre, y centre)
SMD_2X10 = [("J6_Camera", 20.07, 26.67), ("J5_DSI", 82.55, 26.67)]

V = App.Vector
doc = App.newDocument("Arduino_GIGA_R1_WiFi")

BLACK = (0.06, 0.06, 0.06)
CHIP = (0.12, 0.12, 0.13)
METAL = (0.80, 0.80, 0.82)
GOLD = (0.85, 0.70, 0.25)


def add(shape, name, color):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if App.GuiUp:
        obj.ViewObject.ShapeColor = color
    return obj


def box(x0, y0, z0, dx, dy, dz):
    return Part.makeBox(dx, dy, dz, V(x0, y0, z0))


def cbox(cx, cy, z0, dx, dy, dz):
    """Box centred on (cx, cy) in XY."""
    return box(cx - dx / 2, cy - dy / 2, z0, dx, dy, dz)


def pin_grid(x0, y0, cols, rows, pitch=P):
    return [(x0 + i * pitch, y0 + j * pitch) for j in range(rows) for i in range(cols)]


def female_header(pts, pitch, height, z0, tail):
    """Black body with square sockets + gold pins; returns (body, pins)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w = pitch
    body = box(min(xs) - w / 2, min(ys) - w / 2, z0,
               max(xs) - min(xs) + w, max(ys) - min(ys) + w, height)
    sock = Part.makeCompound([cbox(x, y, z0 + 1.0, 1.0, 1.0, height) for x, y in pts])
    body = body.cut(sock)
    zb = -tail if tail else z0           # THT tails poke out under the PCB
    pins = Part.makeCompound([cbox(x, y, zb, PIN_W, PIN_W, z0 + 1.0 - zb) for x, y in pts])
    return body, pins


# ---- PCB ------------------------------------------------------------------
wire = Part.makePolygon([V(x, y, 0) for x, y in OUTLINE + OUTLINE[:1]])
pcb = Part.Face(wire).extrude(V(0, 0, PCB_T))
pcb = pcb.cut(Part.makeCompound([Part.makeCylinder(d / 2, PCB_T + 2, V(x, y, -1))
                                 for x, y, d in HOLES]))
add(pcb, "PCB", (0.05, 0.16, 0.22))

# ---- Headers ----------------------------------------------------------------
for name, xi, yi, cols, rows in FEMALE:
    body, pins = female_header(pin_grid(xi * IN, yi * IN, cols, rows), P, FH_H, PCB_T, TAIL)
    add(body, name, BLACK)
    add(pins, name + "_pins", GOLD)

for name, cx, cy in SMD_2X10:
    pts = pin_grid(cx - P / 2, cy - 4.5 * P, 2, 10)
    body, pins = female_header(pts, P, 6.0, PCB_T, 0)
    add(body, name, BLACK)
    add(pins, name + "_pins", GOLD)

# SPI: 2x3 male header (0.1"), JTAG J8: 2x5 1.27 mm SMD (FTSH-105-01-F-DV).
spi = pin_grid(63.50, 25.40, 2, 3)
add(Part.makeCompound([cbox(x, y, PCB_T, P, P, 2.5) for x, y in spi]), "SPI", BLACK)
add(Part.makeCompound([cbox(x, y, -TAIL, PIN_W, PIN_W, TAIL + PCB_T + 8.5) for x, y in spi]),
    "SPI_pins", GOLD)
jtag = pin_grid(64.08, 14.26, 2, 5, 1.27)
add(cbox(64.72, 16.80, PCB_T, 3.4, 6.35, 1.5), "J8_JTAG", BLACK)
add(Part.makeCompound([cbox(x, y, PCB_T, 0.4, 0.4, 4.3) for x, y in jtag]), "J8_JTAG_pins", GOLD)

# ---- Connectors on the left edge ---------------------------------------------
# J2 USB-A host (TE 292303-7), overhangs the edge ~2 mm.
usba = box(-2.2, 16.85, PCB_T, 14.0, 13.1, 6.6)
usba = usba.cut(box(-3.0, 16.85 + 0.6, PCB_T + 0.6, 12.0, 11.9, 5.4))
add(usba, "J2_USB_A", METAL)
add(box(-1.6, 16.85 + 1.6, PCB_T + 1.4, 11.0, 9.9, 1.8), "J2_USB_A_tongue", (0.05, 0.2, 0.6))

# J12 USB-C (CX90B-16P), stadium shell 8.94 x 3.26.
usbc = box(-1.3, 35.0, PCB_T, 7.35, 8.94, 3.26)
usbc = usbc.makeFillet(1.6, [e for e in usbc.Edges
                             if abs(e.Vertexes[0].Point.x - e.Vertexes[-1].Point.x) > 1])
inner = box(-2.0, 35.4, PCB_T + 0.4, 7.0, 8.14, 2.46)
inner = inner.makeFillet(1.2, [e for e in inner.Edges
                               if abs(e.Vertexes[0].Point.x - e.Vertexes[-1].Point.x) > 1])
add(usbc.cut(inner), "J12_USB_C", METAL)
add(box(-0.8, 37.3, PCB_T + 1.33, 5.5, 4.34, 0.6), "J12_USB_C_tongue", BLACK)

# J15 3.5 mm audio jack.
jack = box(-1.0, 6.4, PCB_T, 13.2, 6.5, 5.2)
jack = jack.fuse(Part.makeCylinder(2.5, 1.2, V(-1.0, 9.65, PCB_T + 2.6), V(-1, 0, 0)))
jack = jack.cut(Part.makeCylinder(1.8, 10, V(1.0, 9.65, PCB_T + 2.6), V(-1, 0, 0)))
add(jack.removeSplitter(), "J15_Audio", BLACK)

# J14 U.FL antenna connector.
ufl = cbox(2.0, 47.0, PCB_T, 2.6, 2.6, 0.5).fuse(
    Part.makeCylinder(1.0, 1.25, V(2.0, 47.0, PCB_T)))
add(ufl.cut(Part.makeCylinder(0.4, 2, V(2.0, 47.0, PCB_T + 0.5))), "J14_UFL", GOLD)

# ---- Buttons (PTS830) ---------------------------------------------------------
for name, cx, cy in [("PB1_RESET", 3.0, 51.0), ("PB2_BOOT0", 3.0, 2.3)]:
    add(cbox(cx, cy, PCB_T, 4.2, 3.2, 1.4), name, METAL)
    add(Part.makeCylinder(0.9, 1.1, V(cx, cy, PCB_T + 1.4)), name + "_cap", BLACK)

# ---- ICs and passives -------------------------------------------------------
# (name, cx, cy, dx, dy, h, colour)
PARTS = [
    ("U1_STM32H747", 41.6, 27.8, 14.0, 14.0, 1.2, CHIP),
    ("U3_SDRAM", 55.5, 27.8, 8.0, 8.0, 1.2, CHIP),
    ("U8_QSPI_Flash", 29.9, 26.0, 5.0, 6.0, 0.6, CHIP),
    ("U5_WiFi_BT_1DX", 14.2, 45.0, 5.2, 5.4, 1.2, METAL),
    ("U4_ATECC608", 22.6, 43.5, 2.0, 3.0, 0.6, CHIP),
    ("U6_3V3_Buck", 25.2, 13.0, 1.5, 2.0, 0.6, CHIP),
    ("U7_5V_Buck", 45.9, 10.4, 2.0, 3.0, 0.8, CHIP),
    ("L_5V", 39.7, 10.4, 4.0, 3.0, 2.0, (0.25, 0.25, 0.27)),
    ("L3", 28.7, 13.2, 1.8, 1.6, 1.0, (0.25, 0.25, 0.27)),
    ("Y3_16MHz", 41.0, 16.8, 3.2, 2.5, 0.8, METAL),
    ("Y2_32k768", 35.4, 16.2, 3.2, 1.5, 0.8, METAL),
    ("DL1_ON", 4.3, 33.1, 1.6, 0.8, 0.6, (0.9, 0.9, 0.9)),
    ("DL2_RGB", 7.7, 2.6, 1.6, 1.6, 0.6, (0.9, 0.9, 0.9)),
    ("D4", 11.4, 32.6, 1.6, 2.6, 1.0, CHIP),
    ("U9_PowerSwitch", 8.0, 38.8, 1.6, 1.6, 0.5, CHIP),
]
for name, cx, cy, dx, dy, h, col in PARTS:
    add(cbox(cx, cy, PCB_T, dx, dy, h), name, col)

doc.recompute()
if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    # Three-quarter view from the USB / audio edge.
    view.setCameraOrientation(App.Rotation(V(0, 0, 1), -55).multiply(
        App.Rotation(V(1, 0, 0), 55)))
    view.fitAll()
    view.saveImage(os.path.join(OUT_DIR, NAME + ".png"), 1200, 900, "White")
doc.saveAs(os.path.join(OUT_DIR, NAME + ".FCStd"))
Part.export(doc.Objects, os.path.join(OUT_DIR, NAME + ".step"))
bb = pcb.BoundBox
print("PCB %.2f x %.2f x %.2f mm" % (bb.XLength, bb.YLength, bb.ZLength))

if App.GuiUp and os.environ.get("FC_BATCH"):
    from PySide import QtCore, QtGui
    App.closeDocument(doc.Name)
    QtCore.QTimer.singleShot(0, QtGui.QApplication.quit)
