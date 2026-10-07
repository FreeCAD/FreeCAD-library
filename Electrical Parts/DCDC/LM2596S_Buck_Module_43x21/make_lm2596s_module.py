# Parametric FreeCAD model: LM2596S DC-DC buck converter module (blue 43 x 21 mm board, Youmile B07ZCRTMXK)
# Licence: CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/)
# Independently drawn approximation. Seller: 43 x 21 x 14 mm incl. potentiometer. Component positions
# scaled from a top-view product photo; component sizes from standard packages (TO-263-5, 3296W, SMA,
# 8 mm electrolytics, 12 x 12 mm shielded inductor). Verify before tight-tolerance use.
# Run: freecad.cmd make_lm2596s_module.py   (or paste into the FreeCAD Python console)
import FreeCAD as App, Part
from FreeCAD import Vector as V
import os

# ---- parameters (mm) ----
PCB_L, PCB_W, PCB_T = 43.2, 21.0, 1.6
HOLE_D = 3.0
HOLES = [(6.65, 18.6), (35.8, 2.3)]                     # mounting holes (diagonal corners)
PAD = 2.0; PAD_HOLE_D = 1.0
PADS = {"IN+": (1.8, 19.2), "IN-": (1.8, 1.8), "OUT+": (41.0, 18.8), "OUT-": (41.0, 1.8)}
IC_X, IC_Y = 14.7, 14.5                                 # TO-263-5 body centre
IC_BODY, IC_H, IC_TAB = (10.1, 9.0), 4.4, (10.4, 1.4)   # body L x W, height, exposed tab L x W
IC_LEAD_PITCH, IC_LEAD_W, IC_LEAD_L = 1.7, 0.8, 4.6
L_X, L_Y, L_SIZE, L_H = 27.1, 7.0, 12.0, 7.0            # inductor
CAP_IN, CAP_OUT = (4.45, 10.6), (38.6, 10.1)            # capacitor centres
CAP_D, CAP_H = 8.0, 12.0
POT_X, POT_Y, POT = 28.5, 17.1, (9.5, 4.8, 10.0)        # 3296W trimmer
DIODE_X, DIODE_Y, DIODE = 12.5, 2.0, (4.4, 2.6, 2.1)    # SS34 SMA
FN = os.environ.get("LM_OUT", os.path.join(os.getcwd(), "LM2596S_Buck_Module_43x21"))

doc = App.newDocument("LM2596S_Module")
# Origin: PCB bottom face, IN- corner. X = length (IN -> OUT), Y = width, Z = up.
box = lambda x0, y0, z0, dx, dy, dz: Part.makeBox(dx, dy, dz, V(x0, y0, z0))
cbox = lambda cx, cy, z0, dx, dy, dz: box(cx - dx/2, cy - dy/2, z0, dx, dy, dz)
cyl = lambda cx, cy, z0, d, h: Part.makeCylinder(d/2, h, V(cx, cy, z0))
Z = PCB_T

pcb = box(0, 0, 0, PCB_L, PCB_W, PCB_T)
for x, y in HOLES: pcb = pcb.cut(cyl(x, y, 0, HOLE_D, PCB_T))
for x, y in PADS.values(): pcb = pcb.cut(cyl(x, y, 0, PAD_HOLE_D, PCB_T))

pads = None
for x, y in PADS.values():
    p = cbox(x, y, Z, PAD, PAD, 0.05).cut(cyl(x, y, Z, PAD_HOLE_D, 0.05))
    pads = p if pads is None else pads.fuse(p)
for x, y in HOLES:
    r = cyl(x, y, Z, HOLE_D + 1.6, 0.05).cut(cyl(x, y, Z, HOLE_D, 0.05))
    pads = pads.fuse(r)

ic = cbox(IC_X, IC_Y, Z, IC_BODY[0], IC_BODY[1], IC_H)
ic = ic.makeChamfer(0.4, [e for e in ic.Edges if abs(e.BoundBox.ZMin - (Z + IC_H)) < 1e-6 and e.BoundBox.ZLength < 1e-6])
metal = cbox(IC_X, IC_Y + IC_BODY[1]/2 + IC_TAB[1]/2, Z, IC_TAB[0], IC_TAB[1], 1.3)  # heat-sink tab
for i in range(5):
    x = IC_X + (i - 2) * IC_LEAD_PITCH
    lead = cbox(x, IC_Y - IC_BODY[1]/2 - IC_LEAD_L/2 + 0.5, Z, IC_LEAD_W, IC_LEAD_L - 1.0, 0.5)
    lead = lead.fuse(cbox(x, IC_Y - IC_BODY[1]/2 - 0.5, Z, IC_LEAD_W, 1.0, 2.0))
    metal = metal.fuse(lead)
metal = metal.removeSplitter()

ind = cbox(L_X, L_Y, Z, L_SIZE, L_SIZE, L_H)
ind = ind.makeFillet(1.5, [e for e in ind.Edges if e.BoundBox.XLength < 1e-6 and e.BoundBox.YLength < 1e-6])
ind = ind.cut(cyl(L_X, L_Y, Z + L_H - 0.3, L_SIZE - 2.0, 0.3))

caps = []
for name, (x, y) in (("CapIn_100uF_50V", CAP_IN), ("CapOut_220uF_35V", CAP_OUT)):
    c = cyl(x, y, Z + 0.3, CAP_D, CAP_H - 0.3)
    c = c.makeFillet(0.5, [e for e in c.Edges if abs(e.BoundBox.ZMax - (Z + CAP_H)) < 1e-6])
    c = c.cut(Part.makeTorus(CAP_D/2 + 0.2, 0.45, V(x, y, Z + 2.0)))  # crimp groove
    caps.append((name, c))

pot = cbox(POT_X, POT_Y, Z, *POT)
pot = pot.fuse(cyl(POT_X - POT[0]/2 + 1.5, POT_Y, Z + POT[2], 2.2, 0.8))  # brass adjust screw
pot = pot.cut(cbox(POT_X - POT[0]/2 + 1.5, POT_Y, Z + POT[2] + 0.4, 0.5, 2.4, 0.4))
diode = cbox(DIODE_X, DIODE_Y, Z, *DIODE)

parts = [("PCB", pcb, (0.05, 0.25, 0.65)), ("Pads", pads, (0.85, 0.85, 0.82)),
         ("LM2596S", ic, (0.1, 0.1, 0.1)), ("LM2596S_TabLeads", metal, (0.8, 0.8, 0.8)),
         ("Inductor_47uH", ind, (0.25, 0.25, 0.27)),
         *[(n, c, (0.82, 0.82, 0.85)) for n, c in caps],
         ("Trimpot_3296W", pot, (0.1, 0.35, 0.85)), ("Diode_SS34", diode, (0.12, 0.12, 0.12))]
objs = []
for name, shp, col in parts:
    o = doc.addObject("Part::Feature", name); o.Shape = shp
    if hasattr(o, "ViewObject") and o.ViewObject: o.ViewObject.ShapeColor = col
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
