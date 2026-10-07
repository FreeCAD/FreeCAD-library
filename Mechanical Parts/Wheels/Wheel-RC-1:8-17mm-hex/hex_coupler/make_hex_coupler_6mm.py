# Parametric FreeCAD model: 6 mm brass hex wheel coupler, 12 mm hex x 18 mm (Amazon B07QNHQGZB)
# Licence: CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/)
# Seller-published dimensions: 6 mm bore, 18 mm length, 11.5 mm body dia, 12 mm hex A/F, M4 set screw,
# M4 axial thread in hex end. Other values estimated from product photos; verify before tight-tolerance use.
# Run: freecad.cmd make_hex_coupler_6mm.py   (or paste into the FreeCAD Python console)
import FreeCAD as App, Part
from FreeCAD import Vector as V
import math, os

# ---- parameters (mm) ----
L = 18.0                  # overall length
BODY_D = 11.5             # round body diameter
HEX_AF, HEX_L = 12.0, 8.0 # hex across flats / hex length (estimated from photo)
HEX_CHAMFER = 0.5         # chamfer on hex end corners
BORE_D, BORE_DEPTH = 6.0, 11.0     # shaft bore from round end
M4_TAP_D = 3.3                     # modelled as M4 tap-drill size (threads not modelled)
SET_Z = 4.0                        # set screw centre from round end
AX_THREAD_DEPTH = L - BORE_DEPTH   # axial M4 from hex end, meets the bore
EDGE_CHAMFER = 0.3
FN = os.environ.get("HC_OUT", os.path.join(os.getcwd(), "Hex_Coupler_6mm_12hex_18L"))

doc = App.newDocument("Hex_Coupler_6mm")
# z=0 is hex end face (wheel side), +Z towards the round end (motor side)

r_corner = HEX_AF / 2 / math.cos(math.radians(30))
pts = [V(r_corner*math.cos(math.radians(60*i)), r_corner*math.sin(math.radians(60*i)), 0) for i in range(7)]
hexa = Part.Face(Part.makePolygon(pts)).extrude(V(0, 0, HEX_L))
# turned chamfer on the hex end: intersect with a cone
cone = Part.makeCone(r_corner - HEX_CHAMFER, r_corner - HEX_CHAMFER + HEX_L, HEX_L)
hexa = hexa.common(cone)

body = Part.makeCylinder(BODY_D/2, L - HEX_L, V(0, 0, HEX_L))
body = body.makeChamfer(EDGE_CHAMFER, [e for e in body.Edges if abs(e.Vertexes[0].Point.z - L) < 1e-6])

c = hexa.fuse(body).removeSplitter()
c = c.cut(Part.makeCylinder(BORE_D/2, BORE_DEPTH, V(0, 0, L - BORE_DEPTH)))
c = c.cut(Part.makeCylinder(M4_TAP_D/2, AX_THREAD_DEPTH + 0.01, V(0, 0, 0)))
c = c.cut(Part.makeCylinder(M4_TAP_D/2, BODY_D/2 + 1, V(0, 0, L - SET_Z), V(1, 0, 0)))

o = doc.addObject("Part::Feature", "HexCoupler"); o.Shape = c
if hasattr(o, "ViewObject") and o.ViewObject: o.ViewObject.ShapeColor = (0.85, 0.68, 0.25)
doc.recompute()
doc.saveAs(FN + ".FCStd")
Part.export([o], FN + ".step")
import Mesh; Mesh.export([o], FN + ".stl")
print("bbox:", c.BoundBox, "valid:", c.isValid(), "solids:", len(c.Solids), "vol:", round(c.Volume, 1))
print("Saved", FN)
