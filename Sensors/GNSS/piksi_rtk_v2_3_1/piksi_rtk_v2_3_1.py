"""Swift Navigation Piksi v2.3.1 RTK GNSS receiver board.

53 x 53 x 1.6 mm PCB, 4 x M3 holes (46 mm square pattern).  Origin: centre of
PCB underside, Z up.  Edge connectors: SMA antenna (+Y), micro-USB (-Y),
two DF13 6-pin UARTs (+X / -X edges).
Run: freecad.cmd piksi_rtk_v2_3_1.py
"""
import os
import sys

sys.path.insert(0, "/home/charles/tmp/claude/freecad_models")
import FreeCAD as App
from fcutil import V, box, rbox_c, cyl, fuse, cut, compound, text, part, feat, save, dump_mesh, HERE

PCB = (0.06, 0.32, 0.16)
SILK = (0.95, 0.95, 0.95)
GOLD = (0.85, 0.70, 0.30)
TIN = (0.80, 0.80, 0.82)
IC = (0.08, 0.08, 0.09)
CREAM = (0.90, 0.85, 0.70)
LED_G, LED_R = (0.1, 0.9, 0.2), (0.95, 0.15, 0.1)

L, T = 53.0, 1.6
doc = App.newDocument("Piksi_v2_3_1")
p = part(doc, "Piksi", None, "Swift Navigation Piksi v2.3.1")
holes = [(x, y) for x in (-23, 23) for y in (-23, 23)]

pcb = rbox_c(0, 0, 0, L, L, T, r=2)
pcb = cut(pcb, [cyl(1.6, 4, (x, y, -1)) for x, y in holes])
feat(doc, p, "PCB", pcb, PCB, "PCB")
feat(doc, p, "HolePads", compound([cut(cyl(3, 0.05, (x, y, T)), cyl(1.6, 1, (x, y, T - 0.5)))
                                   for x, y in holes]), GOLD, "Mounting pads")
Z = T

# RF front-end under a shield can (MAX2769 + SAW filters)
feat(doc, p, "RFShield", cut(box(-24, 6, Z, 20, 16, 2.6), box(-23.8, 6.2, Z - 0.1, 19.6, 15.6, 2.5)),
     TIN, "RF shield can")
# FPGA (Spartan-6 BGA) and MCU (STM32F4 LQFP-64)
feat(doc, p, "FPGA", rbox_c(4, 4, Z, 15, 15, 1.4, r=0.3), IC, "FPGA (Spartan-6)")
mcu = [rbox_c(6, -14, Z, 10, 10, 1.4, r=0.2)]
pins = []
for i in range(16):
    o = -3.75 + i * 0.5
    pins += [box(6 + o - 0.11, -14 - 6, Z, 0.22, 1, 0.15), box(6 + o - 0.11, -14 + 5, Z, 0.22, 1, 0.15),
             box(6 - 6, -14 + o - 0.11, Z, 1, 0.22, 0.15), box(6 + 5, -14 + o - 0.11, Z, 1, 0.22, 0.15)]
feat(doc, p, "MCU", mcu[0], IC, "MCU (STM32F4)")
feat(doc, p, "MCUPins", compound(pins), TIN, "MCU pins")
feat(doc, p, "Flash", rbox_c(-12, -12, Z, 5, 6, 1.0), IC, "Flash")
feat(doc, p, "TCXO", rbox_c(-12, -2, Z, 3.2, 2.5, 1.0, r=0.2), TIN, "TCXO")
feat(doc, p, "Regulators", compound([rbox_c(18, y, Z, 3, 3, 1.0) for y in (-4, 2)]), IC, "Regulators")
feat(doc, p, "Passives", compound(
    [box(x, y, Z, 1.0, 0.5, 0.5) for x in (-2, 0, 14, 16, -18, -16) for y in (-6, -8)]),
    (0.55, 0.45, 0.35), "Passives")

# connectors
sma = fuse([box(-3.2, 20.5, Z, 6.4, 6.0, 6.4),
            cyl(3.1, 9.5, (0, 26.5, Z + 3.2), (0, 1, 0))])
feat(doc, p, "SMA", sma, GOLD, "SMA antenna connector")
feat(doc, p, "MicroUSB", rbox_c(-4, -24.5, Z, 7.5, 5.5, 2.6, r=0.6), TIN, "Micro-USB")
for nm, x in (("UARTA", 23.5), ("UARTB", -23.5)):
    feat(doc, p, nm, cut(rbox_c(x, -6, Z, 4.5, 9.0, 3.6, r=0.3),
                         box(x - 1.6 + (0.8 if x > 0 else -0.8), -10, Z + 0.8, 3.2, 8.0, 3)),
         CREAM, "DF13 %s" % nm)
feat(doc, p, "SWD", compound([box(x, 21.5, Z, 0.6, 0.6, 5.5) for x in (14, 16.54, 19.08)] +
                             [box(x - 0.6, 20.9, Z, 1.8, 1.8, 2.5) for x in (14.3, 16.84, 19.38)]),
     GOLD, "Pin header")
feat(doc, p, "LEDs", compound([box(-18 + i * 3, -21, Z, 1.6, 0.8, 0.6) for i in range(2)]), LED_G, "LEDs (green)")
feat(doc, p, "LEDR", box(-12, -21, Z, 1.6, 0.8, 0.6), LED_R, "LED (red)")
feat(doc, p, "Button", fuse([box(10, 19, Z, 4, 3, 1.5), cyl(0.8, 0.5, (12, 20.5, Z + 1.5))]), TIN, "Reset button")

feat(doc, p, "Silk", compound([text("PIKSI v2.3.1", 2.0, 8, 16.6, Z, 0.03),
                               text("SWIFT NAVIGATION", 1.3, 8, 14.0, Z, 0.03)]), SILK, "Silkscreen")

doc.recompute()
save(doc, os.path.join(HERE, "piksi_rtk_v2_3_1.FCStd"))
dump_mesh(doc, os.path.join(HERE, "preview", "piksi_rtk_v2_3_1.json"))
