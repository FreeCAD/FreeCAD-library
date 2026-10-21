# FreeCAD model of a TS35 x 7.5 top-hat DIN rail (EN 60715), the standard
# rail for modular circuit breakers. Slotted steel, 1 mm thick. Bend radii
# are ignored (sharp corners).
#
# Run:  freecad din_rail.py   (GUI: keeps colours, saves preview PNG)
#       freecad.cmd din_rail.py (headless: geometry only)
# Writes din_rail.FCStd and din_rail.step next to this script.

import os
import FreeCAD as App
import Part

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- Parameters (mm) ------------------------------------------------------
LENGTH = 100.0              # rail length (cut to suit; 1 pole MCB = 18 mm)
WIDTH = 35.0                # overall flange width
HAT_W = 27.0                # outside width of the raised section
DEPTH = 7.5                 # panel to flange top (15.0 for TS35 x 15)
THICK = 1.0                 # sheet thickness
SLOT_L, SLOT_W = 15.0, 5.2  # mounting slots in the web, along the rail
SLOT_PITCH = 25.0
SLOTTED = True

ZINC = (0.78, 0.80, 0.82)

V = App.Vector
doc = App.newDocument("DIN_Rail")


def add(shape, name, color):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if App.GuiUp:
        obj.ViewObject.ShapeColor = color
    return obj


# Origin: centre of the rail's start, web on the panel at z=0..THICK,
# flanges at z=DEPTH-THICK..DEPTH, rail runs along +X, profile in YZ.
w, h, t, d = WIDTH / 2, HAT_W / 2, THICK, DEPTH
outline = [(-w, d), (-h + t, d), (-h + t, t), (h - t, t), (h - t, d), (w, d),
           (w, d - t), (h, d - t), (h, 0), (-h, 0),
           (-h, d - t), (-w, d - t), (-w, d)]
profile = Part.Face(Part.makePolygon([V(0, y, z) for y, z in outline]))
rail = profile.extrude(V(LENGTH, 0, 0))

n_slots = 0
if SLOTTED:
    # Slots on the centre line, pattern centred on the rail length.
    n_slots = int((LENGTH - SLOT_L) // SLOT_PITCH) + 1
    x0 = (LENGTH - (n_slots - 1) * SLOT_PITCH) / 2
    for k in range(n_slots):
        cx = x0 + k * SLOT_PITCH
        slot = Part.makeBox(SLOT_L - SLOT_W, SLOT_W, t + 2,
                            V(cx - (SLOT_L - SLOT_W) / 2, -SLOT_W / 2, -1))
        for ex in (-1, 1):
            slot = slot.fuse(Part.makeCylinder(SLOT_W / 2, t + 2,
                                               V(cx + ex * (SLOT_L - SLOT_W) / 2, 0, -1)))
        rail = rail.cut(slot)

rail = add(rail.removeSplitter(), "DIN_Rail_TS35x%g" % DEPTH, ZINC)

doc.recompute()
if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.viewIsometric()
    view.fitAll()
    view.saveImage(os.path.join(OUT_DIR, "din_rail.png"), 1200, 900, "White")
doc.saveAs(os.path.join(OUT_DIR, "din_rail.FCStd"))
Part.export(doc.Objects, os.path.join(OUT_DIR, "din_rail.step"))
rail = rail.Shape
bb = rail.BoundBox
print("Rail %.1f x %.1f x %.1f mm, %d slots, volume %.0f mm3"
      % (bb.XLength, bb.YLength, bb.ZLength, n_slots, rail.Volume))

if App.GuiUp and os.environ.get("FC_BATCH"):
    from PySide import QtCore, QtGui
    App.closeDocument(doc.Name)
    QtCore.QTimer.singleShot(0, QtGui.QApplication.quit)
