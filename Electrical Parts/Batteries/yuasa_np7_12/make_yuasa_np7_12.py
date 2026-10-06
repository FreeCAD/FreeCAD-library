# Parametric FreeCAD model: Yuasa NP7-12 12 V 7 Ah sealed lead acid battery, Faston F1 (187 / 4.75 mm) terminals
# Licence: CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/)
# Independently drawn approximation, not a Yuasa drawing. Datasheet: 151 L x 65 W x 97.5 H (over terminals),
# terminal layout 4 (both at one end), Faston 187 tab 4.70 W x 0.80 T x 6.35 H with 1.5 x 2.5 slot.
# Case height, lid split, terminal ledge and positions estimated from product photos; verify before use.
# Run: freecad.cmd make_yuasa_np7_12.py   (or paste into the FreeCAD Python console)
import FreeCAD as App, Part
from FreeCAD import Vector as V
import os

# ---- parameters (mm) ----
L, W = 151.0, 65.0
H_TOTAL = 97.5                  # over terminals
CASE_H = 94.0                   # top of lid (estimated)
LID_T = 13.0                    # black lid thickness
LEDGE_L, LEDGE_DROP = 20.0, 3.9 # terminal ledge at x=0 end: length / depth below lid top
TAB_W, TAB_T, TAB_H = 4.70, 0.80, 6.35   # Faston 187 tab above ledge
TAB_SLOT_W, TAB_SLOT_H, TAB_SLOT_TOP = 1.5, 2.5, 1.9  # slot size / gap from tab top to slot top
TAB_X = 9.0                     # tab centre from terminal end
TAB_Y_POS, TAB_Y_NEG = W - 13.0, 13.0
BASE_BOSS = (8.0, 6.0, 1.0)     # moulded boss under each tab (x, y, height)
EDGE_R = 1.5
FN = os.environ.get("BAT_OUT", os.path.join(os.getcwd(), "Yuasa_NP7-12_F1"))

doc = App.newDocument("Yuasa_NP7_12")
# Origin: bottom corner below the terminal end. X = length, Y = width, Z = up.
box = lambda x0, y0, z0, dx, dy, dz: Part.makeBox(dx, dy, dz, V(x0, y0, z0))
vert_edges = lambda s: [e for e in s.Edges if abs(e.BoundBox.XLength) < 1e-6 and abs(e.BoundBox.YLength) < 1e-6]

case = box(0, 0, 0, L, W, CASE_H - LID_T)
case = case.makeFillet(EDGE_R, vert_edges(case))
lid = box(0, 0, CASE_H - LID_T, L, W, LID_T)
lid = lid.makeFillet(EDGE_R, vert_edges(lid))
lid = lid.cut(box(-1, -1, CASE_H - LEDGE_DROP, LEDGE_L + 1, W + 2, LEDGE_DROP + 1))
lid = lid.cut(box(40, 8, CASE_H - 0.6, L - 50, W - 16, 0.6))  # label recess on lid top

z_ledge = CASE_H - LEDGE_DROP
parts = [("Case", case, (0.88, 0.88, 0.86)), ("Lid", lid, (0.08, 0.08, 0.08))]
for name, y, col in (("TerminalPos", TAB_Y_POS, (0.8, 0.1, 0.1)), ("TerminalNeg", TAB_Y_NEG, (0.1, 0.1, 0.1))):
    bx, by, bh = BASE_BOSS
    parts.append((name + "Boss", box(TAB_X - bx/2, y - by/2, z_ledge, bx, by, bh), col))
    tab = box(TAB_X - TAB_W/2, y - TAB_T/2, z_ledge + bh, TAB_W, TAB_T, H_TOTAL - z_ledge - bh)
    tab = tab.cut(box(TAB_X - TAB_SLOT_W/2, y - TAB_T, H_TOTAL - TAB_SLOT_TOP - TAB_SLOT_H, TAB_SLOT_W, 2*TAB_T, TAB_SLOT_H))
    for sx in (-1, 1):  # entry chamfers on tab top corners
        c = Part.makePolygon([V(TAB_X + sx*TAB_W/2, y - TAB_T, H_TOTAL - 0.8), V(TAB_X + sx*(TAB_W/2 - 0.8), y - TAB_T, H_TOTAL),
                              V(TAB_X + sx*(TAB_W/2 + 1), y - TAB_T, H_TOTAL + 1), V(TAB_X + sx*(TAB_W/2 + 1), y - TAB_T, H_TOTAL - 0.8),
                              V(TAB_X + sx*TAB_W/2, y - TAB_T, H_TOTAL - 0.8)])
        tab = tab.cut(Part.Face(c).extrude(V(0, 2*TAB_T, 0)))
    parts.append((name, tab, (0.85, 0.8, 0.6)))

objs = []
for name, shp, c in parts:
    o = doc.addObject("Part::Feature", name); o.Shape = shp
    if hasattr(o, "ViewObject") and o.ViewObject: o.ViewObject.ShapeColor = c
    objs.append(o)
doc.recompute()
doc.saveAs(FN + ".FCStd")
Part.export(objs, FN + ".step")
import Mesh; Mesh.export(objs, FN + ".stl")
print("bbox:", Part.makeCompound([o.Shape for o in objs]).BoundBox)
for i, a in enumerate(objs):
    print(a.Name, "valid" if a.Shape.isValid() else "INVALID", len(a.Shape.Solids), round(a.Shape.Volume, 1),
          [b.Name for b in objs[i+1:] if a.Shape.common(b.Shape).Volume > 1e-3])
print("Saved", FN)
