"""HUAREW 1-channel 5V relay module with optocoupler isolation, high/low level trigger.

Run headless:  freecad.cmd huarew_1ch_relay_optocoupler.py
Produces huarew_1ch_relay_optocoupler.FCStd.

Source: Amazon UK B0B52RPY43 (model HR-RELAY-10-5V-UK).  Board 50 x 25 mm (listing
dimension photo), red PCB, 4 corner mounting holes.  Left edge: 3-way screw
terminal NO / COM / NC (top to bottom); right edge: 3-way terminal IN / DC- / DC+.
SRD-05VDC-SL-C relay (10A 250VAC), SMD optocoupler, L/H trigger jumper, green
power LED and red relay-status LED.

Origin: centre of the PCB underside; X along the 50 mm length, Z up.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
from fcutil import V, box, rbox, cyl, fuse, cut, compound, text, part, feat, save, dump_mesh, HERE

OUT = os.path.join(HERE, "huarew_1ch_relay_optocoupler.FCStd")

PCB_C = (0.78, 0.08, 0.08)
SILK = (0.96, 0.96, 0.96)
TIN = (0.80, 0.80, 0.82)
RELAY_C = (0.12, 0.33, 0.85)
TERM_C = (0.10, 0.42, 0.86)
BLACK = (0.06, 0.06, 0.07)
GOLD = (0.85, 0.68, 0.25)

L, W, TH = 50.0, 25.0, 1.6
ZT = TH

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
doc = App.newDocument("HUAREW_1ch_Relay")
mod = part(doc, "RelayModule", None, "HUAREW 1-ch relay module")
mod.Placement = App.Placement(V(-L / 2, -W / 2, 0), App.Rotation())

holes = [(3.0, 3.0), (L - 3.0, 3.0), (3.0, W - 3.0), (L - 3.0, W - 3.0)]
pcb = rbox(0, 0, 0, L, W, TH, r=1.0)
pcb = cut(pcb, [cyl(1.5, 4, (x, y, -1)) for x, y in holes])
feat(doc, mod, "PCB", pcb, PCB_C, "PCB")
feat(doc, mod, "HoleRings", compound([cut(cyl(2.7, TH + 0.08, (x, y, -0.04)),
                                          cyl(1.5, 4, (x, y, -1))) for x, y in holes]),
     TIN, "Mounting hole rings")

# screw terminals
tl_body, tl_scr = place(terminal(3), 2.4, 5.0, "-x")
tr_body, tr_scr = place(terminal(3), L - 2.4 - 7.5, 5.0, "+x")
feat(doc, mod, "TerminalOut", tl_body, TERM_C, "Terminal NO/COM/NC")
feat(doc, mod, "TerminalOutScrews", tl_scr, TIN, "Terminal screws (output)")
feat(doc, mod, "TerminalIn", tr_body, TERM_C, "Terminal IN/DC-/DC+")
feat(doc, mod, "TerminalInScrews", tr_scr, TIN, "Terminal screws (input)")

# relay
rb, rp = relay_srd(10.6, 5.5, "x")
feat(doc, mod, "Relay", rb, RELAY_C, "Relay SRD-05VDC-SL-C")
feat(doc, mod, "RelayPrint", rp, (0.05, 0.08, 0.25), "Relay print")

# optocoupler, transistor, diode
ob, op = chip(34.0, 9.0, 4.4, 3.6, 2.0, legs=2, leg_axis="x")
tb, tp = chip(33.0, 17.0, 2.9, 1.3, 1.0, legs=0)
db, dp = chip(33.5, 21.0, 2.7, 1.6, 1.0)
feat(doc, mod, "ICs", compound([ob, tb, db]), BLACK, "Optocoupler, transistor, diode")
legs = op + [box(32.0, 17.5, ZT, 0.4, 1.2, 0.3), box(33.6, 17.5, ZT, 0.4, 1.2, 0.3),
             box(32.8, 15.3, ZT, 0.4, 1.2, 0.3),
             box(31.8, 20.5, ZT, 0.5, 1.0, 0.4), box(34.7, 20.5, ZT, 0.5, 1.0, 0.4)]
feat(doc, mod, "Leads", compound(legs), TIN, "Leads")

# passives and LEDs
res = [passive(31.0, 12.5, "y"), passive(36.6, 12.5, "y"), passive(36.6, 16.0, "y"),
       passive(36.6, 23.7, "x"), passive(30.5, 23.0, "x"), passive(36.0, 5.5, "x")]
feat(doc, mod, "Resistors", compound([r[0] for r in res]), BLACK, "Resistors")
feat(doc, mod, "ResistorEnds", compound([e for r in res for e in r[1]]), TIN, "Resistor ends")
caps = [passive(30.5, 18.5, "y")]
feat(doc, mod, "Caps", compound([c[0] for c in caps]), (0.72, 0.58, 0.40), "Capacitors")
feat(doc, mod, "CapEnds", compound([e for c in caps for e in c[1]]), TIN, "Capacitor ends")
feat(doc, mod, "LEDPower", box(40.6, 21.6, ZT, 2.0, 1.25, 0.7), (0.2, 0.9, 0.3, 0.2),
     "Power LED (green)")
feat(doc, mod, "LEDRelay", box(37.4, 18.6, ZT, 2.0, 1.25, 0.7), (0.95, 0.15, 0.1, 0.2),
     "Relay LED (red)")

# L/H trigger jumper (3 pins along X, jumper on H side)
hp, hpins = header(33.6, 2.6, 3, "x")
feat(doc, mod, "TriggerHeader", hp, BLACK, "Trigger select header")
feat(doc, mod, "TriggerPins", hpins, GOLD, "Header pins")
feat(doc, mod, "TriggerJumper", box(33.6 + 2.54 - 1.25, 2.6 - 1.25, ZT + 2.5 + 0.2, 5.04, 2.5,
                                    6.0), BLACK, "Jumper (H)")

# silkscreen
silk = [text("NO", 1.5, 1.3, 17.5, ZT, 0.03, rot=((1.3, 17.5, 0), (0, 0, 1), 90)),
        text("COM", 1.5, 1.3, 12.5, ZT, 0.03, rot=((1.3, 12.5, 0), (0, 0, 1), 90)),
        text("NC", 1.5, 1.3, 7.5, ZT, 0.03, rot=((1.3, 7.5, 0), (0, 0, 1), 90)),
        text("IN", 1.5, L - 1.3, 17.5, ZT, 0.03, rot=((L - 1.3, 17.5, 0), (0, 0, 1), 90)),
        text("DC-", 1.5, L - 1.3, 12.5, ZT, 0.03, rot=((L - 1.3, 12.5, 0), (0, 0, 1), 90)),
        text("DC+", 1.5, L - 1.3, 7.5, ZT, 0.03, rot=((L - 1.3, 7.5, 0), (0, 0, 1), 90)),
        text("1 Relay  Module", 1.8, 20.0, 3.9, ZT, 0.03),
        text("high/low level trigger", 1.5, 20.0, 1.8, ZT, 0.03),
        text("L", 1.3, 32.0, 4.9, ZT, 0.03), text("H", 1.3, 40.8, 4.9, ZT, 0.03),
        text("PWR", 1.2, 38.6, 21.6, ZT, 0.03),
        text("LED", 1.2, 39.0, 15.5, ZT, 0.03, rot=((39.0, 15.5, 0), (0, 0, 1), 90))]
feat(doc, mod, "Silkscreen", compound([s for s in silk if s is not None]), SILK, "Silkscreen")

doc.recompute()
save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "huarew_1ch_relay_optocoupler.json"))
