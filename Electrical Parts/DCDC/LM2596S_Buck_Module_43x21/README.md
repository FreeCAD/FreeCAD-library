# LM2596S DC-DC buck converter module (43 x 21 mm blue board) — Youmile B07ZCRTMXK

Files: `LM2596S_Buck_Module_43x21.FCStd` (FreeCAD), `.step`, `.stl`, plus parametric generator
`make_lm2596s_module.py` (run with `freecad.cmd make_lm2596s_module.py`).

Licence: Creative Commons Attribution 3.0 Unported (CC BY 3.0) — https://creativecommons.org/licenses/by/3.0/

Independently drawn approximation. Seller: 43 x 21 x 14 mm including potentiometer.
Modelled height is 13.6 mm (1.6 mm PCB + 12 mm capacitors).
Component positions scaled from a top-view product photo; component sizes from standard packages:
LM2596S TO-263-5, 12 x 12 x 7 mm "470" (47 uH) shielded inductor, 8 x 12 mm 100 uF / 220 uF capacitors,
3296W trimmer, SS34 (SMA) diode. Small SMD parts (resistors, LED) not modelled.
Mounting: 2 x 3.0 mm holes at (6.65, 18.6) and (35.8, 2.3) — diagonal corners, ~29.2 x 16.3 mm apart.
Solder pads (1.0 mm holes): IN- (1.8, 1.8), IN+ (1.8, 19.2), OUT- (41.0, 1.8), OUT+ (41.0, 18.8).
Origin: PCB bottom face at the IN- corner; X = length (IN -> OUT), Y = width, Z = up.

There is a KiCAD model available here:
https://github.com/Jana-Marie/KiCAD-libs/blob/master/otter.pretty/LM2596-DC-DC.kicad_mod
