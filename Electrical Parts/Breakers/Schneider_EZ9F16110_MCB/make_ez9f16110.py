# Parametric FreeCAD model: Schneider Electric Easy9 MCB EZ9F16110 (1P, 10 A, B curve, 6 kA)
# Licence: CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/)
# Independently drawn approximation, not a Schneider drawing. Datasheet dimensions: 18 W x 82 H x 72 D mm,
# 1 module (2 x 9 mm pitch), DIN rail clip-on, tunnel terminals top & bottom. Profile proportions
# scaled from a side-view product photo and DIN 43880 (45 mm front collar); verify before tight-tolerance use.
# Run: freecad.cmd make_ez9f16110.py   (or paste into the FreeCAD Python console)
import FreeCAD as App, Part
from FreeCAD import Vector as V
import os

# ---- parameters (mm) ----
W, H, D = 18.0, 82.0, 72.0        # overall width / height / depth (depth incl. toggle)
SHOULDER_Z = 48.5                 # terminal shoulder face, from DIN rail mounting plane
COLLAR_H, FRONT_Z = 45.0, 64.5    # front collar height (DIN 43880) / front face
RAIL_W, RAIL_RECESS = 35.2, 1.2   # TS35 rail channel in back face
CLIP_W, CLIP_L, CLIP_T, CLIP_TAB = 9.0, 17.0, 3.0, 1.5  # green rail clip (bottom) and pull tab
TERM_Y = 34.0                     # terminal screw centre from device centre (top and bottom)
SCREW_HOLE_D, SCREW_HEAD_D = 8.0, 6.5
TUNNEL_W, TUNNEL_D, TUNNEL_DEPTH, TUNNEL_Z0 = 7.5, 7.5, 14.0, 34.0  # wire entry on top/bottom faces
TOG_RECESS_W, TOG_RECESS_Y0, TOG_RECESS_Y1, TOG_RECESS_DEPTH = 13.0, -16.0, 2.0, 6.0
TOG_W, TOG_T, TOG_Y = 10.5, 6.0, -7.0  # toggle lever width / thickness / centre height
WIN_W, WIN_H, WIN_Y = 6.0, 3.0, 8.0    # contact position indicator window
FN = os.environ.get("MCB_OUT", os.path.join(os.getcwd(), "Schneider_EZ9F16110_MCB"))

doc = App.newDocument("Schneider_EZ9F16110")
# Origin: DIN rail centre line on the mounting plane. X = width, Y = up (line side), Z = out of panel.
box = lambda x0, y0, z0, dx, dy, dz: Part.makeBox(dx, dy, dz, V(x0, y0, z0))

body = box(-W/2, -H/2, 0, W, H, SHOULDER_Z)
body = body.fuse(box(-W/2, -COLLAR_H/2, SHOULDER_Z, W, COLLAR_H, FRONT_Z - SHOULDER_Z)).removeSplitter()
body = body.cut(box(-W/2, -RAIL_W/2, 0, W, RAIL_W, RAIL_RECESS))
body = body.cut(box(-CLIP_W/2, -H/2, 0, CLIP_W, CLIP_L, CLIP_T))  # pocket for clip
for s in (1, -1):
    yt = s * TERM_Y
    body = body.cut(Part.makeCylinder(SCREW_HOLE_D/2, SHOULDER_Z - TUNNEL_Z0 - TUNNEL_D, V(0, yt, TUNNEL_Z0 + TUNNEL_D)))
    y_face = s * H/2
    body = body.cut(box(-TUNNEL_W/2, y_face - (TUNNEL_DEPTH if s > 0 else 0), TUNNEL_Z0, TUNNEL_W, TUNNEL_DEPTH, TUNNEL_D))
body = body.cut(box(-TOG_RECESS_W/2, TOG_RECESS_Y0, FRONT_Z - TOG_RECESS_DEPTH, TOG_RECESS_W, TOG_RECESS_Y1 - TOG_RECESS_Y0, TOG_RECESS_DEPTH))
body = body.cut(box(-WIN_W/2, WIN_Y - WIN_H/2, FRONT_Z - 1.0, WIN_W, WIN_H, 1.0))
body = body.removeSplitter()

toggle = box(-TOG_W/2, TOG_Y - TOG_T/2, FRONT_Z - TOG_RECESS_DEPTH, TOG_W, TOG_T, D - FRONT_Z + TOG_RECESS_DEPTH)
toggle = toggle.makeFillet(1.0, [e for e in toggle.Edges if abs(e.BoundBox.ZMin - D) < 1e-6 and abs(e.BoundBox.ZMax - D) < 1e-6])

clip = box(-CLIP_W/2, -H/2 - CLIP_TAB, 0, CLIP_W, CLIP_L + CLIP_TAB, CLIP_T)
clip = clip.cut(box(-CLIP_W/2 + 2.5, -H/2 - CLIP_TAB, 0, CLIP_W - 5, CLIP_TAB, CLIP_T - 1.0))  # screwdriver slot

parts = [("Body", body, (0.84, 0.85, 0.83)), ("Toggle", toggle, (0.15, 0.15, 0.16)), ("RailClip", clip, (0.2, 0.75, 0.25))]
for s, name in ((1, "ScrewLine"), (-1, "ScrewLoad")):
    yt = s * TERM_Y
    z0 = TUNNEL_Z0 + TUNNEL_D
    scr = Part.makeCylinder(SCREW_HEAD_D/2, SHOULDER_Z - 2.0 - z0, V(0, yt, z0))
    scr = scr.cut(box(-SCREW_HEAD_D/2, yt - 0.4, SHOULDER_Z - 3.5, SCREW_HEAD_D, 0.8, 1.5))
    scr = scr.cut(box(-0.4, yt - SCREW_HEAD_D/2, SHOULDER_Z - 3.5, 0.8, SCREW_HEAD_D, 1.5))
    parts.append((name, scr, (0.75, 0.75, 0.72)))

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
