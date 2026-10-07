"""SainSmart 8-Channel 5V Relay Module.

Run headless:  freecad.cmd sainsmart_8ch_5v_relay.py
Produces sainsmart_8ch_5v_relay.FCStd.

Source: sainsmart.com product page photos (layout).  The page gives no
dimensions; the board uses the widely quoted 138 x 56 mm outline with 4 x
dia 3.1 mounting holes 3 mm in from each corner (132 x 50 mm pattern).
Layout as photographed: 8 x 3-way screw terminals (NO/COM/NC, in four 6-way
blocks) along one long edge, 8 SONGLE SRD-05VDC-SL-C relays, then per channel a
PC817 optocoupler, driver transistor, flyback diode and red LED; along the
opposite edge the 10-pin input header (GND, IN1..IN8, VCC) and the 3-pin
GND / VCC / JD-VCC header with its jumper.

Origin: centre of the PCB underside; X along the 138 mm length, terminals on +Y, Z up.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
from fcutil import V, box, rbox, cyl, fuse, cut, compound, text, part, feat, save, dump_mesh, HERE

OUT = os.path.join(HERE, "sainsmart_8ch_5v_relay.FCStd")

PCB_C = (0.12, 0.55, 0.82)
SILK = (0.96, 0.96, 0.96)
TIN = (0.80, 0.80, 0.82)
RELAY_C = (0.22, 0.50, 0.88)
TERM_C = (0.16, 0.48, 0.84)
BLACK = (0.06, 0.06, 0.07)
GOLD = (0.85, 0.68, 0.25)

L, W, TH = 138.0, 56.0, 1.6
ZT = TH
N = 8
PITCH = 16.5                       # channel pitch (relay spacing)
X0 = (L - N * PITCH) / 2           # left edge of channel 1

# ------------------------------------------------------------ component helpers


def place(shapes, x0, y0, facing="-y"):
    """Rotate shapes built facing -Y together, moving the first one's bbox min corner to (x0, y0)."""
    ang = {"-y": 0, "-x": -90, "+x": 90, "+y": 180}[facing]
    out = []
    for sh in shapes:
        s = sh.copy()
        if ang:
            s.rotate(V(0, 0, 0), V(0, 0, 1), ang)
        out.append(s)
    bb = out[0].BoundBox
    for s in out:
        s.translate(V(x0 - bb.XMin, y0 - bb.YMin, 0))
    return out


def terminal(n, pitch=5.0, d=7.5, h=10.0):
    """Screw terminal block (KF301 style): (body, screws), wire entries on the -Y face."""
    body = box(0, 0, ZT, n * pitch, d, h)
    body = cut(body, [box(-1, -1, ZT + h - 2.5, n * pitch + 2, 2.5 + 1, 3)])
    screws = []
    for i in range(n):
        cx = i * pitch + pitch / 2
        body = cut(body, [box(cx - 1.6, -1, ZT + 1.2, 3.2, 4.5, 3.2),
                          cyl(1.7, 4, (cx, d * 0.62, ZT + h - 3.5))])
        head = cut(cyl(1.5, 1.2, (cx, d * 0.62, ZT + h - 2.4)),
                   box(cx - 1.6, d * 0.62 - 0.3, ZT + h - 1.6, 3.2, 0.6, 1))
        screws += [head, box(cx - 1.3, 2.2, ZT + 1.0, 2.6, 2.6, 3.6)]
    return body, compound(screws)


def relay_srd(x0, y0, along="x"):
    """SRD-05VDC-SL-C relay, 19 x 15.5 x 15.3; returns (body, print)."""
    lx, ly = (19.0, 15.5) if along == "x" else (15.5, 19.0)
    body = rbox(x0, y0, ZT, lx, ly, 15.3, r=0.4, r_top=0.5)
    zt = ZT + 15.3
    cx, cy = x0 + lx / 2, y0 + ly / 2
    rot = None if along == "x" else ((cx, cy, 0), (0, 0, 1), 90)
    prn = [text("SRD-05VDC-SL-C", 1.35, cx, cy - 4.5, zt, 0.05, rot=rot),
           text("10A 250VAC  10A 125VAC", 0.9, cx, cy - 1.5, zt, 0.05, rot=rot),
           text("10A 30VDC   10A 28VDC", 0.9, cx, cy + 0.5, zt, 0.05, rot=rot),
           text("SONGLE", 1.8, cx, cy + 4.5, zt, 0.05, rot=rot)]
    return body, compound([p for p in prn if p is not None])


def chip(x, y, l, w, h, legs=0, leg_axis="y"):
    """Small SMD package centred at (x, y); legs on the two sides normal to leg_axis."""
    body = box(x - l / 2, y - w / 2, ZT + 0.1, l, w, h)
    pins = []
    if legs:
        span = (l if leg_axis == "y" else w) * 0.7
        for k in range(legs):
            t = -span / 2 + span * k / max(legs - 1, 1) if legs > 1 else 0
            for s in (-1, 1):
                if leg_axis == "y":
                    pins.append(box(x + t - 0.2, y + s * w / 2 - 0.6, ZT, 0.4, 1.2, 0.3))
                else:
                    pins.append(box(x + s * l / 2 - 0.6, y + t - 0.2, ZT, 1.2, 0.4, 0.3))
    return body, pins


def passive(x, y, along="x", l=2.0, w=1.25, h=0.5):
    """0805 resistor/cap: (body, end caps)."""
    if along == "y":
        l, w = w, l
    body = box(x - l / 2, y - w / 2, ZT, l, w, h)
    if along == "x":
        ends = [box(x - l / 2, y - w / 2, ZT, 0.35, w, h + 0.02),
                box(x + l / 2 - 0.35, y - w / 2, ZT, 0.35, w, h + 0.02)]
    else:
        ends = [box(x - l / 2, y - w / 2, ZT, l, 0.35, h + 0.02),
                box(x - l / 2, y + w / 2 - 0.35, ZT, l, 0.35, h + 0.02)]
    return body, ends


def header(x0, y0, n, along="x", pitch=2.54):
    """Straight male header, first pin centre at (x0, y0)."""
    dx, dy = (pitch, 0) if along == "x" else (0, pitch)
    plastic, pins = [], []
    for i in range(n):
        cx, cy = x0 + i * dx, y0 + i * dy
        plastic.append(box(cx - 1.27, cy - 1.27, ZT, 2.54, 2.54, 2.5))
        pins.append(box(cx - 0.32, cy - 0.32, -1.5, 0.64, 0.64, ZT + 2.5 + 6.0 + 1.5))
    return fuse(plastic), compound(pins)


# ------------------------------------------------------------------- build
doc = App.newDocument("SainSmart_8ch_Relay")
mod = part(doc, "RelayModule", None, "SainSmart 8-channel 5V relay module")
mod.Placement = App.Placement(V(-L / 2, -W / 2, 0), App.Rotation())

holes = [(3.0, 3.0), (L - 3.0, 3.0), (3.0, W - 3.0), (L - 3.0, W - 3.0)]
pcb = rbox(0, 0, 0, L, W, TH, r=1.0)
pcb = cut(pcb, [cyl(1.55, 4, (x, y, -1)) for x, y in holes])
feat(doc, mod, "PCB", pcb, PCB_C, "PCB")
feat(doc, mod, "HoleRings", compound([cut(cyl(2.8, TH + 0.08, (x, y, -0.04)),
                                          cyl(1.55, 4, (x, y, -1))) for x, y in holes]),
     TIN, "Mounting hole rings")

# terminals: four 6-way blocks (two channels each), wire entries facing the +Y edge
tb, ts = [], []
for k in range(N // 2):
    blk_x = X0 + k * 2 * PITCH + (2 * PITCH - 30.0) / 2
    b, s = place(terminal(6), blk_x, W - 7.5, "+y")
    tb.append(b)
    ts.append(s)
feat(doc, mod, "Terminals", compound(tb), TERM_C, "Screw terminals (NO/COM/NC x8)")
feat(doc, mod, "TerminalScrews", compound(ts), TIN, "Terminal screws")

relays, prints = [], []
ics, leads, res_b, res_e, leds = [], [], [], [], []
silk = []
for i in range(N):
    cx = X0 + (i + 0.5) * PITCH
    rb, rp = relay_srd(cx - 7.75, W - 8.0 - 19.0, "y")
    relays.append(rb)
    prints.append(rp)
    # optocoupler (DIP-4), transistor, diode
    ob, op = chip(cx - 1.5, 17.5, 4.6, 6.5, 3.5, legs=2, leg_axis="x")
    qb, _ = chip(cx + 4.5, 23.5, 2.9, 1.3, 1.0)
    dbb, _ = chip(cx + 4.5, 12.0, 3.6, 1.6, 1.1)
    ics += [ob, qb, dbb]
    leads += op + [box(cx + 3.4, 24.1, ZT, 0.4, 1.0, 0.3), box(cx + 5.2, 24.1, ZT, 0.4, 1.0, 0.3),
                   box(cx + 4.3, 22.0, ZT, 0.4, 1.0, 0.3),
                   box(cx + 2.4, 11.5, ZT, 0.6, 1.0, 0.4), box(cx + 6.0, 11.5, ZT, 0.6, 1.0, 0.4)]
    for (px, py, al) in ((cx + 4.5, 18.0, "x"), (cx - 6.3, 17.5, "y"), (cx - 6.3, 12.0, "y")):
        b, e = passive(px, py, al)
        res_b.append(b)
        res_e += e
    leds.append(box(cx - 2.5, 10.4, ZT, 2.0, 1.25, 0.7))
    silk.append(text("K%d" % (i + 1), 1.4, cx, W - 28.6, ZT, 0.03))
    silk.append(text("IN%d" % (i + 1), 1.0, cx - 2.5 + 1.0, 9.0, ZT, 0.03))
feat(doc, mod, "Relays", compound(relays), RELAY_C, "Relays SRD-05VDC-SL-C x8")
feat(doc, mod, "RelayPrint", compound(prints), (0.05, 0.08, 0.25), "Relay print")
feat(doc, mod, "ICs", compound(ics), BLACK, "Optocouplers, transistors, diodes")
feat(doc, mod, "Leads", compound(leads), TIN, "Leads")
feat(doc, mod, "Resistors", compound(res_b), BLACK, "Resistors")
feat(doc, mod, "ResistorEnds", compound(res_e), TIN, "Resistor ends")
feat(doc, mod, "LEDs", compound(leds), (0.95, 0.15, 0.1, 0.2), "Channel LEDs (red)")
feat(doc, mod, "LEDPower", box(116.0, 10.4, ZT, 2.0, 1.25, 0.7), (0.95, 0.15, 0.1, 0.2),
     "Power LED")

# input header GND, IN1..IN8, VCC and the JD-VCC jumper header
HX = 64.0
hp, hpins = header(HX, 4.0, 10, "x")
jp, jpins = header(121.0, 4.0, 3, "x")
feat(doc, mod, "InputHeader", fuse([hp, jp]), BLACK, "Headers")
feat(doc, mod, "HeaderPins", compound([hpins, jpins]), GOLD, "Header pins")
feat(doc, mod, "JDVCCJumper", box(121.0 + 2.54 - 1.25, 4.0 - 1.25, ZT + 2.5 + 0.2, 5.04, 2.5, 6.0),
     (0.15, 0.35, 0.85), "JD-VCC jumper")
for k, name in enumerate(["GND"] + ["IN%d" % n for n in range(1, 9)] + ["VCC"]):
    silk.append(text(name, 0.8, HX + k * 2.54, 1.3, ZT, 0.03))
for k, name in enumerate(["GND", "VCC", "JD-VCC"]):
    silk.append(text(name, 0.8, 121.0 + k * 2.54, 1.3, ZT, 0.03))
silk += [text("8 Relay Module", 2.4, 30.0, 4.0, ZT, 0.03),
         text("SainSMART", 2.4, 100.0, 4.0, ZT, 0.03)]
feat(doc, mod, "Silkscreen", compound([s for s in silk if s is not None]), SILK, "Silkscreen")

doc.recompute()
save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "sainsmart_8ch_5v_relay.json"))
