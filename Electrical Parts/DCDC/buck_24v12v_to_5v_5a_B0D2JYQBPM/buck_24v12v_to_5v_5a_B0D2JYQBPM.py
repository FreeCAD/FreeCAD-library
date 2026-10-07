"""24V/12V to 5V 5A synchronous buck converter board (Amazon UK B0D2JYQBPM, tinshow,
board marked HW-688; sold as a 2-pack — this is one board).

Run headless:  freecad.cmd buck_24v12v_to_5v_5a_B0D2JYQBPM.py
Produces buck_24v12v_to_5v_5a_B0D2JYQBPM.FCStd.

Source: listing text (63 x 27 x 10 mm, 9-36V in, 5.2V 5A out) and the "product size"
top-view photo, from which component positions are scaled.  Input side (left):
2-way screw terminal (Input +/-) and 5.5 x 2.1 mm DC jack; output side (right):
2-way screw terminal (Output +/-) and USB-A socket.  330 shielded inductor,
100uF/50V and 470uF/16V SMD electrolytics, two D4184 DPAK MOSFETs, controller,
fast-charge ID chip, reverse-protection diode, PWR LED.

Origin: centre of the PCB underside; X along the 63 mm length (input at -X), Z up.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir()
                else "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
from fcutil import V, box, rbox, cyl, fuse, cut, compound, text, part, feat, save, dump_mesh, HERE

OUT = os.path.join(HERE, "buck_24v12v_to_5v_5a_B0D2JYQBPM.FCStd")

PCB_C = (0.06, 0.28, 0.56)
SILK = (0.96, 0.96, 0.96)
TIN = (0.80, 0.80, 0.82)
STEEL = (0.75, 0.76, 0.78)
TERM_C = (0.10, 0.45, 0.88)
BLACK = (0.06, 0.06, 0.07)
INDUCTOR = (0.42, 0.42, 0.44)
ALU = (0.82, 0.83, 0.85)

L, W, TH = 63.0, 27.0, 1.6
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




def ecap(x, y, d=8.0, h=8.4, label=""):
    """SMD aluminium electrolytic: (black base, can, top print)."""
    base = box(x - d / 2 - 0.3, y - d / 2 - 0.3, ZT, d + 0.6, d + 0.6, 1.4)
    base = cut(base, [box(x - d / 2 - 1, y - d / 2 - 1, ZT - 1, 1.6, 1.6, 4)])  # chamfered corner
    can = cut(cyl(d / 2, h - 1.4, (x, y, ZT + 1.4)),
              [cut(cyl(d / 2 + 1, 0.6, (x, y, ZT + 2.4)), cyl(d / 2 - 0.4, 2, (x, y, ZT + 2)))])
    prn = [cut(cyl(d / 2 - 0.05, 0.05, (x, y, ZT + h)), cyl(d / 2 - 0.9, 1, (x, y, ZT + h - 0.5)))
           .common(box(x - d, y - d / 2, ZT + h - 1, d * 2, d * 0.35, 2))]
    for k, s in enumerate(label.split()):
        t = text(s, 1.5, x, y + 0.8 - k * 2.0, ZT + h, 0.05)
        if t is not None:
            prn.append(t)
    return base, can, compound(prn)


def dpak(x, y, label="D4184"):
    """TO-252 (DPAK) MOSFET centred at (x, y), tab toward +Y: (body, metal)."""
    body = box(x - 3.3, y - 3.0, ZT + 0.1, 6.6, 6.1, 2.3)
    metal = [box(x - 2.7, y + 2.6, ZT, 5.4, 1.4, 0.5)]
    metal += [box(x + dx - 0.4, y - 5.0, ZT, 0.8, 2.2, 0.5) for dx in (-2.28, 2.28)]
    t = text(label, 1.0, x, y, ZT + 2.4, 0.03)
    return body, compound(metal), t


# ------------------------------------------------------------------- build
doc = App.newDocument("Buck_5V_5A")
mod = part(doc, "BuckBoard", None, "Buck converter 24V/12V -> 5V 5A")
mod.Placement = App.Placement(V(-L / 2, -W / 2, 0), App.Rotation())

feat(doc, mod, "PCB", rbox(0, 0, 0, L, W, TH, r=0.8), PCB_C, "PCB")

# screw terminals (2-way)
ib, iscr = place(terminal(2), 0.0, 17.5, "-x")
ob, oscr = place(terminal(2), L - 7.5, 17.5, "+x")
feat(doc, mod, "TerminalIn", ib, TERM_C, "Input terminal (9-36V)")
feat(doc, mod, "TerminalOut", ob, TERM_C, "Output terminal (5V)")
feat(doc, mod, "TerminalScrews", compound([iscr, oscr]), TIN, "Terminal screws")

# DC jack 5.5 x 2.1, opening facing -X, overhanging the edge slightly
jack = box(-1.0, 1.2, ZT, 14.0, 9.0, 9.0)
jack = cut(jack, cyl(3.05, 11.0, (-2.0, 5.7, ZT + 4.8), (1, 0, 0)))
feat(doc, mod, "DCJack", jack, BLACK, "DC jack 5.5x2.1")
feat(doc, mod, "DCJackPin", fuse([cyl(1.0, 10.0, (0.0, 5.7, ZT + 4.8), (1, 0, 0)),
                                  box(11.5, 4.7, ZT + 9.0, 2.5, 2.0, 0.3)]), TIN, "DC jack pin")

# USB-A socket, opening facing +X
ux0, uy0, ul, uw, uh = 50.5, 0.5, 14.0, 13.1, 5.7
shell = cut(box(ux0, uy0, ZT, ul, uw, uh),
            box(ux0 + 1.0, uy0 + 0.4, ZT + 0.4, ul, uw - 0.8, uh - 0.8))
feat(doc, mod, "USBShell", shell, STEEL, "USB-A socket")
feat(doc, mod, "USBTongue", box(ux0 + 2.0, uy0 + 1.0, ZT + 0.4 + 1.0, ul - 3.0, uw - 2.0, 1.8),
     (0.92, 0.92, 0.92), "USB tongue")

# inductor 330
feat(doc, mod, "Inductor", rbox(36.5, 0.8, ZT, 11.5, 11.5, 7.0, r=1.0, r_top=0.5), INDUCTOR,
     "Inductor 33uH (330)")
feat(doc, mod, "InductorPrint", text("330", 4.0, 42.25, 6.55, ZT + 7.0, 0.05,
                                     rot=((42.25, 6.55, 0), (0, 0, 1), 90)), BLACK,
     "Inductor print")

# electrolytics
c1 = ecap(12.0, 21.5, label="100 50V")
c2 = ecap(47.6, 21.5, label="470 16V")
feat(doc, mod, "CapBases", compound([c1[0], c2[0]]), BLACK, "Capacitor bases")
feat(doc, mod, "CapCans", compound([c1[1], c2[1]]), ALU, "Electrolytic capacitors")
feat(doc, mod, "CapPrint", compound([c1[2], c2[2]]), (0.15, 0.15, 0.18), "Capacitor print")

# MOSFETs, controller, fast-charge chip, diode
q1 = dpak(38.0, 20.5)
q2 = dpak(30.5, 5.5)
u1, u1l = chip(25.5, 20.5, 4.9, 3.9, 1.5, legs=4, leg_axis="y")
u5, u5l = chip(19.5, 5.5, 2.9, 1.6, 1.0, legs=3, leg_axis="y")
d1, _ = chip(9.8, 13.6, 4.3, 2.6, 2.1)
feat(doc, mod, "ICs", compound([q1[0], q2[0], u1, u5, d1]), BLACK,
     "MOSFETs, controller, charge-ID chip, diode")
feat(doc, mod, "Leads", compound([q1[1], q2[1]] + u1l + u5l
                                 + [box(7.3, 13.0, ZT, 0.8, 1.2, 0.5),
                                    box(11.5, 13.0, ZT, 0.8, 1.2, 0.5)]), TIN, "Leads")
feat(doc, mod, "ICPrint", compound([q1[2], q2[2]]), (0.6, 0.6, 0.62), "IC print")

# small passives
pp = [(17.5, 24.0, "x"), (17.5, 21.5, "x"), (20.5, 17.0, "y"), (22.5, 15.5, "x"),
      (29.5, 24.5, "x"), (31.5, 20.5, "y"), (31.5, 15.0, "x"), (27.0, 15.0, "x"),
      (24.5, 11.0, "y"), (18.0, 9.5, "x"), (14.5, 3.0, "y"), (22.5, 2.5, "x"),
      (34.0, 11.5, "y"), (43.0, 15.5, "x"), (50.0, 15.5, "x"), (52.5, 24.0, "x")]
pb, pe = [], []
caps_b = []
for k, (x, y, al) in enumerate(pp):
    b, e = passive(x, y, al, l=1.6, w=0.8, h=0.45)
    (caps_b if k % 3 == 0 else pb).append(b)
    pe += e
feat(doc, mod, "Resistors", compound(pb), BLACK, "Resistors")
feat(doc, mod, "Caps", compound(caps_b), (0.72, 0.58, 0.40), "Ceramic capacitors")
feat(doc, mod, "PassiveEnds", compound(pe), TIN, "Passive ends")
feat(doc, mod, "LED", box(52.0, 25.2, ZT, 1.6, 0.8, 0.6), (0.95, 0.15, 0.1, 0.2), "PWR LED")

silk = [text("HW-688", 1.4, 23.5, 6.0, ZT, 0.03, rot=((23.5, 6.0, 0), (0, 0, 1), 90)),
        text("PWR", 1.0, 52.8, 23.6, ZT, 0.03),
        text("D1", 0.9, 9.8, 15.6, ZT, 0.03),
        text("U5", 0.9, 19.5, 7.6, ZT, 0.03)]
feat(doc, mod, "Silkscreen", compound([s for s in silk if s is not None]), SILK, "Silkscreen")

doc.recompute()
save(doc, OUT)
dump_mesh(doc, os.path.join(HERE, "preview", "buck_24v12v_to_5v_5a_B0D2JYQBPM.json"))
