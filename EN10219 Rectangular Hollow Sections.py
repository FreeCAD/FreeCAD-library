# -*- coding:utf-8 -*-
import FreeCAD, FreeCADGui, Part, Draft, math, MeshPart, Mesh, Drawing
from PyQt4 import QtGui,QtCore
from FreeCAD import Base
from FreeCAD import Vector
import ImportGui
import Mesh
import os

App=FreeCAD
Gui=FreeCADGui

param = FreeCAD.ParamGet('User parameter:Plugins/parts_library')
s=param.GetString('destination')
print('User parameter:Plugins/partlib : destination : ',s)

if s<>'':
    LIBRARYPATH = s
else:
    folderDialog = QtGui.QFileDialog.getExistingDirectory(None,u"Choose folder library")
    param.SetString('destination',folderDialog)
    s=param.GetString('destination')
    LIBRARYPATH = s

directory =LIBRARYPATH+'/Mechanical Parts/'
if not os.path.exists(directory):
    os.mkdir(directory)
directory =LIBRARYPATH+'/Mechanical Parts/Profiles EN/'
if not os.path.exists(directory):
    os.mkdir(directory)
directory =LIBRARYPATH+'/Mechanical Parts/Profiles EN/EN10219 Rectangular Hollow Sections/'
if not os.path.exists(directory):
    os.mkdir(directory)

Table = (
 	 ("Rectangular hollow section 50x25x2.5 EN10219 S235JRH",	50,	25,	2.5, 	3.75, 	2.5), 	       ("Rectangular hollow section 50x25x3 EN10219 S235JRH",		50,	25,	3,	4.5,	3),
 	 ("Rectangular hollow section 50x30x2.5 EN10219 S235JRH",	50,	30,	2.5, 	3.75,	2.5), 
 	 ("Rectangular hollow section 50x30x3 EN10219 S235JRH",		50,	30,	3,	4.5, 	3),
 	 ("Rectangular hollow section 50x30x3.2 EN10219 S235JRH",	50,	30,	3.2, 	4.8,	3.2), 
 	 ("Rectangular hollow section 50x30x3.6 EN10219 S235JRH",	50,	30,	3.6,	5.4, 	3.6), 
 	 ("Rectangular hollow section 50x30x4 EN10219 S235JRH",		50,	30,	4,	6,	4),
 	 ("Rectangular hollow section 50x30x5 EN10219 S235JRH",		50,	30,	5,	7.5, 	5),
 	 ("Rectangular hollow section 60x40x2.5 EN10219 S235JRH",	60,	40,	2.5, 	3.75, 	2.5), 
 	 ("Rectangular hollow section 60x40x3 EN10219 S235JRH",		60,	40,	3,	4.5, 	3),
 	 ("Rectangular hollow section 60x40x3.2 EN10219 S235JRH",	60,	40,	3.2, 	4.8, 	3.2), 
 	 ("Rectangular hollow section 60x40x3.6 EN10219 S235JRH",	60,	40,	3.6, 	5.4, 	3.6), 
 	 ("Rectangular hollow section 60x40x4 EN10219 S235JRH",		60,	40,	4,	6,	4),
 	 ("Rectangular hollow section 60x40x5 EN10219 S235JRH",		60,	40,	5,	7.5, 	5),
 	 ("Rectangular hollow section 60x40x6 EN10219 S235JRH",		60,	40,	6,	9,	6),
 	 ("Rectangular hollow section 60x40x6.3 EN10219 S235JRH",	60,	40,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 80x40x3 EN10219 S235JRH",		80,	40,	3,	4.5, 	3),
 	 ("Rectangular hollow section 80x40x3.2 EN10219 S235JRH",	80,	40,	3.2, 	4.8, 	3.2), 
 	 ("Rectangular hollow section 80x40x3.6 EN10219 S235JRH",	80,	40,	3.6, 	5.4, 	3.6), 
 	 ("Rectangular hollow section 80x40x4 EN10219 S235JRH",		80,	40,	4,	6,	4),
 	 ("Rectangular hollow section 80x40x5 EN10219 S235JRH",		80,	40,	5,	7.5, 	5),
 	 ("Rectangular hollow section 80x40x6 EN10219 S235JRH",		80,	40,	6,	9,	6),
 	 ("Rectangular hollow section 80x40x6.3 EN10219 S235JRH",	80,	40,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 80x40x8 EN10219 S235JRH",		80,	40,	8,	12,	8),
 	 ("Rectangular hollow section 76.2 x50.8 x3 EN10219 S235JRH",	76.2, 	50.8, 	3,	4.5, 	3),
 	 ("Rectangular hollow section 76.2 x50.8 x3.2 EN10219 S235JRH",	76.2, 	50.8, 	3.2, 	4.8, 	3.2), 
 	 ("Rectangular hollow section 76.2 x50.8 x3.6 EN10219 S235JRH",	76.2, 	50.8, 	3.6, 	5.4, 	3.6), 
 	 ("Rectangular hollow section 76.2 x50.8 x4 EN10219 S235JRH",	76.2,	50.8, 	4,	6,	4),
 	 ("Rectangular hollow section 76.2 x50.8 x5 EN10219 S235JRH",	76.2,	50.8, 	5,	7.5, 	5),
 	 ("Rectangular hollow section 76.2 x50.8 x6 EN10219 S235JRH",	76.2, 	50.8, 	6,	9,	6),
 	 ("Rectangular hollow section 76.2 x50.8 x6.3 EN10219 S235JRH",	76.2, 	50.8, 	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 76.2 x50.8 x8 EN10219 S235JRH",	76.2, 	50.8, 	8,	12,	8),
 	 ("Rectangular hollow section 90x50x3 EN10219 S235JRH",		90,	50,	3,	4.5, 	3),
 	 ("Rectangular hollow section 90x50x3.2 EN10219 S235JRH",	90,	50,	3.2, 	4.8, 	3.2), 
 	 ("Rectangular hollow section 90x50x3.6 EN10219 S235JRH",	90,	50,	3.6, 	5.4, 	3.6), 
 	 ("Rectangular hollow section 90x50x4 EN10219 S235JRH",		90,	50,	4,	6,	4),
 	 ("Rectangular hollow section 90x50x5 EN10219 S235JRH",		90,	50,	5,	7.5, 	5),
 	 ("Rectangular hollow section 90x50x6 EN10219 S235JRH",		90,	50,	6,	9,	6),
 	 ("Rectangular hollow section 90x50x6.3 EN10219 S235JRH",	90,	50,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 90x50x8 EN10219 S235JRH",		90,	50,	8,	12,	8),
 	 ("Rectangular hollow section 100x50x3 EN10219 S235JRH",		100,	50,	3,	4.5, 	3),
 	 ("Rectangular hollow section 100x50x3.2 EN10219 S235JRH",	100,	50,	3.2, 	4.8, 	3.2), 
 	 ("Rectangular hollow section 100x50x3.6 EN10219 S235JRH",	100,	50,	3.6, 	5.4, 	3.6), 
 	 ("Rectangular hollow section 100x50x4 EN10219 S235JRH",		100,	50,	4,	6,	4),
 	 ("Rectangular hollow section 100x50x5 EN10219 S235JRH",		100,	50,	5,	7.5, 	5),
 	 ("Rectangular hollow section 100x50x6 EN10219 S235JRH",		100,	50,	6,	9,	6),
 	 ("Rectangular hollow section 100x50x6.3 EN10219 S235JRH",	100,	50,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 100x50x8 EN10219 S235JRH",		100,	50,	8,	12,	8),
 	 ("Rectangular hollow section 100x60x3 EN10219 S235JRH",		100,	60,	3,	4.5, 	3),
 	 ("Rectangular hollow section 100x60x3.2 EN10219 S235JRH",	100,	60,	3.2, 	4.8, 	3.2), 
 	 ("Rectangular hollow section 100x60x3.6 EN10219 S235JRH",	100,	60,	3.6, 	5.4, 	3.6), 
 	 ("Rectangular hollow section 100x60x4 EN10219 S235JRH",		100,	60,	4,	6,	4),
 	 ("Rectangular hollow section 100x60x5 EN10219 S235JRH",		100,	60,	5,	7.5, 	5),
 	 ("Rectangular hollow section 100x60x6 EN10219 S235JRH",		100,	60,	6,	9,	6),
 	 ("Rectangular hollow section 100x60x6.3 EN10219 S235JRH",	100,	60,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 100x60x8 EN10219 S235JRH",		100,	60,	8,	12,	8),
 	 ("Rectangular hollow section 120x60x3.6 EN10219 S235JRH",	120,	60,	3.6, 	5.4, 	3.6), 
 	 ("Rectangular hollow section 120x60x4 EN10219 S235JRH",		120,	60,	4,	6,	4),
 	 ("Rectangular hollow section 120x60x5 EN10219 S235JRH",		120,	60,	5,	7.5, 	5),
 	 ("Rectangular hollow section 120x60x6 EN10219 S235JRH",		120,	60,	6,	9,	6),
 	 ("Rectangular hollow section 120x60x6.3 EN10219 S235JRH",	120,	60,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 120x60x8 EN10219 S235JRH",		120,	60,	8,	12,	8),
 	 ("Rectangular hollow section 120x60x10 EN10219 S235JRH",	120,	60,	10,	12,	8),
 	 ("Rectangular hollow section 120x80x3.6 EN10219 S235JRH",	120,	80,	3.6, 	5.4, 	3.6), 
 	 ("Rectangular hollow section 120x80x4 EN10219 S235JRH",		120,	80,	4,	6,	4),
 	 ("Rectangular hollow section 120x80x5 EN10219 S235JRH",		120,	80,	5,	7.5, 	5),
 	 ("Rectangular hollow section 120x80x6 EN10219 S235JRH",		120,	80,	6,	9,	6),
 	 ("Rectangular hollow section 120x80x6.3 EN10219 S235JRH",	120,	80,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 120x80x8 EN10219 S235JRH",		120,	80,	8,	12,	8),
 	 ("Rectangular hollow section 120x80x10 EN10219 S235JRH",	120,	80,	10,	15,	10),
 	 ("Rectangular hollow section 140x80x4 EN10219 S235JRH",		140,	80,	4,	6,	4),
 	 ("Rectangular hollow section 140x80x5 EN10219 S235JRH",		140,	80,	5,	7.5, 	5),
 	 ("Rectangular hollow section 140x80x6 EN10219 S235JRH",		140,	80,	6,	9,	6),
 	 ("Rectangular hollow section 140x80x6.3 EN10219 S235JRH",	140,	80,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 140x80x8 EN10219 S235JRH",		140,	80,	8,	12,	8),
 	 ("Rectangular hollow section 140x80x10 EN10219 S235JRH",	140,	80,	10,	15,	10),
 	 ("Rectangular hollow section 150x100x4 EN10219 S235JRH",	150,	100,	4,	6,	4),
 	 ("Rectangular hollow section 150x100x5 EN10219 S235JRH",	150,	100,	5,	7.5, 	5),
 	 ("Rectangular hollow section 150x100x6 EN10219 S235JRH",	150,	100,	6,	9,	6),
 	 ("Rectangular hollow section 150x100x6.3 EN10219 S235JRH",	150,	100,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 150x100x8 EN10219 S235JRH",	150,	100,	8,	12,	8),
 	 ("Rectangular hollow section 150x100x10 EN10219 S235JRH",	150,	100,	10,	15,	10),
 	 ("Rectangular hollow section 150x100x12 EN10219 S235JRH",	150,	100,	12,	18,	12),
 	 ("Rectangular hollow section 150x100x12.5 EN10219 S235JRH",	150,	100,	12.5, 	18.75, 	12.5),
 	 ("Rectangular hollow section 160x80x4 EN10219 S235JRH",		160,	80,	4,	6,	4),
 	 ("Rectangular hollow section 160x80x5 EN10219 S235JRH",		160,	80,	5,	7.5, 	5),
 	 ("Rectangular hollow section 160x80x6 EN10219 S235JRH",		160,	80,	6,	9,	6),
 	 ("Rectangular hollow section 160x80x6.3 EN10219 S235JRH",	160,	80,	6.3, 	9.45, 	6.3),
 	 ("Rectangular hollow section 160x80x8 EN10219 S235JRH",		160,	80,	8,	12,	8),
 	 ("Rectangular hollow section 160x80x10 EN10219 S235JRH",	160,	80,	10,	15,	10),
 	 ("Rectangular hollow section 160x80x12 EN10219 S235JRH",	160,	80,	12,	18,	12),
 	 ("Rectangular hollow section 160 x80x12.5 EN10219 S235JRH",	160,	80,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 180x100x4 EN10219 S235JRH",	180,	100,	4,	6,	4),
 	 ("Rectangular hollow section 180x100x5 EN10219 S235JRH",	180,	100,	5,	7.5, 	5),
 	 ("Rectangular hollow section 180x100x6 EN10219 S235JRH",	180,	100,	6,	9,	6),
 	 ("Rectangular hollow section 180x100x6.3 EN10219 S235JRH",	180,	100,	6.3, 	9.45, 	6.3),
 	 ("Rectangular hollow section 180x100x8 EN10219 S235JRH",	180,	100,	8,	12,	8),
 	 ("Rectangular hollow section 180x100x10 EN10219 S235JRH",	180,	100,	10,	15,	10),
 	 ("Rectangular hollow section 180x100x12 EN10219 S235JRH",	180,	100,	12,	18,	12),
 	 ("Rectangular hollow section 180x100x12.5 EN10219 S235JRH",	180,	100,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 200x100x4 EN10219 S235JRH",	200,	100,	4,	7.5, 	5),
 	 ("Rectangular hollow section 200x100x5 EN10219 S235JRH",	200,	100,	5,	7.5, 	5),
 	 ("Rectangular hollow section 200x100x6 EN10219 S235JRH",	200,	100,	6,	9,	6),
 	 ("Rectangular hollow section 200x100x6.3 EN10219 S235JRH",	200,	100,	6.3, 	9.45, 	6.3),
 	 ("Rectangular hollow section 200x100x8 EN10219 S235JRH",	200,	100,	8,	12,	8),
 	 ("Rectangular hollow section 200x100x10 EN10219 S235JRH",	200,	100,	10,	15,	10),
 	 ("Rectangular hollow section 200x100x12 EN10219 S235JRH",	200,	100,	12,	18,	12),
 	 ("Rectangular hollow section 200x100x12.5 EN10219 S235JRH",	200,	100,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 200x100x16 EN10219 S235JRH",	200,	100,	16,	24,	16),
 	 ("Rectangular hollow section 200x120x6 EN10219 S235JRH",	200,	120,	6,	9.45, 	6.3),
 	 ("Rectangular hollow section 200x120x6.3 EN10219 S235JRH",	200,	120,	6.3, 	12,	8),
 	 ("Rectangular hollow section 200x120x8 EN10219 S235JRH",	200,	120,	8,	15,	10),
 	 ("Rectangular hollow section 200x120x10 EN10219 S235JRH",	200,	120,	10,	18,	12),
 	 ("Rectangular hollow section 200x120x12 EN10219 S235JRH",	200,	120,	12,	18.75, 	12.5), 
 	 ("Rectangular hollow section 200x120x12.5 EN10219 S235JRH",	200,	120,	12.5, 	24,	16),
 	 ("Rectangular hollow section 250x150x5 EN10219 S235JRH",	250,	150,	5,	7.5, 	5),
 	 ("Rectangular hollow section 250x150x6 EN10219 S235JRH",	250,	150,	6,	9,	6),
 	 ("Rectangular hollow section 250 x150x6.3 EN10219 S235JRH",	250,	150,	6.3, 	9.45, 	6.3),
 	 ("Rectangular hollow section 250x150x8 EN10219 S235JRH",	250,	150,	8,	12,	8),
 	 ("Rectangular hollow section 250x150x10 EN10219 S235JRH",	250,	150,	10,	15,	10),
 	 ("Rectangular hollow section 250x150x12 EN10219 S235JRH",	250,	150,	12,	18,	12),
 	 ("Rectangular hollow section 250x150x12.5 EN10219 S235JRH",	250,	150,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 250x150x16 EN10219 S235JRH",	250,	150,	16,	24,	16),
 	 ("Rectangular hollow section 260x180x6 EN10219 S235JRH",	260,	180,	6,	9,	6),
 	 ("Rectangular hollow section 260x180x6.3 EN10219 S235JRH",	260,	180,	6.3, 	9.45, 	6.3),
 	 ("Rectangular hollow section 260x180x8 EN10219 S235JRH",	260,	180,	8,	12,	8),
 	 ("Rectangular hollow section 260x180x10 EN10219 S235JRH",	260,	180,	10,	15,	10),
 	 ("Rectangular hollow section 260x180x12 EN10219 S235JRH",	260,	180,	12,	18,	12),
 	 ("Rectangular hollow section 260x180x12.5 EN10219 S235JRH",	260,	180,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 260x180x16 EN10219 S235JRH",	260,	180,	16,	24,	16),
 	 ("Rectangular hollow section 300x200x5 EN10219 S235JRH",	300,	200,	5,	7.5, 	5),
 	 ("Rectangular hollow section 300x200x6 EN10219 S235JRH",	300,	200,	6,	9,	6),
 	 ("Rectangular hollow section 300x200x6.3 EN10219 S235JRH",	300,	200,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 300x200x8 EN10219 S235JRH",	300,	200,	8,	12,	8),
 	 ("Rectangular hollow section 300x200x10 EN10219 S235JRH",	300,	200,	10,	15,	10),
 	 ("Rectangular hollow section 300x200x12 EN10219 S235JRH",	300,	200,	12,	18,	12),
 	 ("Rectangular hollow section 300x200x12.5 EN10219 S235JRH",	300,	200,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 300x200x16 EN10219 S235JRH",	300,	200,	16,	24,	16),
 	 ("Rectangular hollow section 350x250x6 EN10219 S235JRH",	350,	250,	6,	9,	6),
 	 ("Rectangular hollow section 350x250x6.3 EN10219 S235JRH",	350,	250,	6.3, 	9.45, 	6.3),
 	 ("Rectangular hollow section 350x250x8 EN10219 S235JRH",	350,	250,	8,	12,	8),
 	 ("Rectangular hollow section 350x250x10 EN10219 S235JRH",	350,	250,	10,	15,	10),
 	 ("Rectangular hollow section 350 x250x12 EN10219 S235JRH",	350,	250,	12,	18,	12),
 	 ("Rectangular hollow section 350x250x12.5 EN10219 S235JRH",	350,	250,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 350x250x16 EN10219 S235JRH",	350,	250,	16,	24,	16),
 	 ("Rectangular hollow section 400x200x6 EN10219 S235JRH",	400,	200,	6,	9,	6),
 	 ("Rectangular hollow section 400x200x6.3 EN10219 S235JRH",	400,	200,	6.3, 	9.45, 	6.3), 
 	 ("Rectangular hollow section 400x200x8 EN10219 S235JRH",	400,	200,	8,	12,	8),
 	 ("Rectangular hollow section 400x200x10 EN10219 S235JRH",	400,	200,	10,	15,	10),
 	 ("Rectangular hollow section 400x200x12 EN10219 S235JRH",	400,	200,	12,	18,	12),
 	 ("Rectangular hollow section 400x200x12.5 EN10219 S235JRH",	400,	200,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 400x200x16 EN10219 S235JRH",	400,	200,	16,	24,	16),
 	 ("Rectangular hollow section 450x250x8 EN10219 S235JRH",	450,	250,	8,	12,	8),
 	 ("Rectangular hollow section 450x250x10 EN10219 S235JRH",	450,	250,	10,	15,	10),
 	 ("Rectangular hollow section 450x250x12 EN10219 S235JRH",	450,	250,	12,	18,	12),
 	 ("Rectangular hollow section 450x250x12.5 EN10219 S235JRH",	450,	250,	12.5, 	18.75, 	12.5), 
 	 ("Rectangular hollow section 450x250x16 EN10219 S235JRH",	450,	250,	16,	24,	16),
 	 ("Rectangular hollow section 500x300x8 EN10219 S235JRH",	500,	300,	8,	12,	8),
 	 ("Rectangular hollow section 500x300x10 EN10219 S235JRH",	500,	300,	10,	15,	10),
 	 ("Rectangular hollow section 500x300x12 EN10219 S235JRH",	500,	300,	12,	18,	12),
 	 ("Rectangular hollow section 500x300x12.5 EN10219 S235JRH",	500,	300,	12.5, 	18.75, 	12.5),
 	 ("Rectangular hollow section 500x300x16 EN10219 S235JRH",	500,	300,	16,	24,	16),
 	 ("Rectangular hollow section 500x300x20 EN10219 S235JRH",	500,	300,	20,	30,	20))






for data in Table:
    print data[0]
    doc=FreeCAD.newDocument("Bar")
    sk1=doc.addObject('Sketcher::SketchObject','Sketch')
    sk1.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation  (0.000000,0.000000,0.000000,1.000000))

    sk1.addGeometry(Part.Line(App.Vector(-2.000000,2.000000,0),App.Vector(2.000000,2.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(2.000000,2.000000,0),App.Vector(2.000000,-2.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(2.000000,-2.000000,0),App.Vector(-2.000000,-2.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(-2.000000,-2.000000,0),App.Vector(-2.000000,2.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',0)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',2)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',1)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',3)) 
    sk1.addGeometry(Part.Line(App.Vector(-3.000000,3.000000,0),App.Vector(3.000000,3.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(3.000000,3.000000,0),App.Vector(3.000000,-3.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(3.000000,-3.000000,0),App.Vector(-3.000000,-3.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(-3.000000,-3.000000,0),App.Vector(-3.000000,3.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',7,2,4,1)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',4)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',6)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',5)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',7)) 
    sk1.fillet(3,0,App.Vector(-2.000000,1.501889,0),App.Vector(-1.547679,2.000000,0),0.454633)
    sk1.fillet(0,1,App.Vector(1.767467,2.000000,0),App.Vector(2.000000,1.593468,0),0.232533)
    sk1.fillet(1,2,App.Vector(2.000000,-1.337048,0),App.Vector(1.730836,-2.000000,0),0.476989)
    sk1.fillet(2,3,App.Vector(-1.291259,-2.000000,0),App.Vector(-2.000000,-1.685047,0),0.504246)
    sk1.fillet(4,5,App.Vector(2.664938,3.000000,0),App.Vector(3.000000,2.582517,0),0.335062)
    sk1.fillet(5,6,App.Vector(3.000000,-2.674096,0),App.Vector(2.738200,-3.000000,0),0.269534)
    sk1.fillet(6,7,App.Vector(-2.390202,-3.000000,0),App.Vector(-3.000000,-2.637465,0),0.438829)
    sk1.fillet(7,4,App.Vector(-3.000000,2.435992,0),App.Vector(-2.664938,3.000000,0),0.405811)
    sk1.addConstraint(Sketcher.Constraint('Equal',9,8)) 
    sk1.addConstraint(Sketcher.Constraint('Equal',9,11)) 
    sk1.addConstraint(Sketcher.Constraint('Equal',9,10)) 
    sk1.addConstraint(Sketcher.Constraint('Equal',12,15)) 
    sk1.addConstraint(Sketcher.Constraint('Equal',12,14)) 
    sk1.addConstraint(Sketcher.Constraint('Equal',12,13)) 
    sk1.addConstraint(Sketcher.Constraint('Symmetric',4,2,6,1,-1)) 
    sk1.addConstraint(Sketcher.Constraint('Symmetric',7,2,5,1,-2)) 
    sk1.delConstraint(6)
    sk1.addConstraint(Sketcher.Constraint('DistanceY',4,2,6,1,-6.116362)) 
    sk1.setDatum(31,App.Units.Quantity('-6.116360 mm'))
    sk1.addConstraint(Sketcher.Constraint('DistanceX',7,2,5,1,6.049826)) 
    sk1.setDatum(32,App.Units.Quantity('6.049830 mm'))
    sk1.addConstraint(Sketcher.Constraint('Symmetric',3,2,1,1,-2)) 
    sk1.addConstraint(Sketcher.Constraint('Symmetric',0,2,2,1,-1)) 
    sk1.delConstraint(2)
    sk1.addConstraint(Sketcher.Constraint('DistanceY',0,2,4,2,0.937142)) 
    sk1.setDatum(34,App.Units.Quantity('0.937142 mm'))
    sk1.addConstraint(Sketcher.Constraint('DistanceX',5,2,1,2,-1.122059)) 
    sk1.setDatum(35,App.Units.Quantity('-1.122060 mm'))
    sk1.addConstraint(Sketcher.Constraint('Radius',9,0.501904)) 
    sk1.setDatum(36,App.Units.Quantity('0.501904 mm'))
    sk1.addConstraint(Sketcher.Constraint('Radius',12,0.463752)) 
    sk1.setDatum(37,App.Units.Quantity('0.463752 mm'))
    sk1.delConstraint(0)
    sk1.delConstraint(2)

    sk1.setDatum(28,App.Units.Quantity(str(-data[1])+' mm'))
    App.ActiveDocument.recompute()
    sk1.setDatum(29,App.Units.Quantity(str(data[2])+' mm'))
    App.ActiveDocument.recompute()
    sk1.setDatum(32,App.Units.Quantity(str(data[3])+' mm'))
    App.ActiveDocument.recompute()
    sk1.setDatum(33,App.Units.Quantity(str(-data[3])+' mm'))
    App.ActiveDocument.recompute()
    sk1.setDatum(35,App.Units.Quantity(str(data[4])+' mm'))
    App.ActiveDocument.recompute()
    sk1.setDatum(34,App.Units.Quantity(str(data[5])+' mm'))
    App.ActiveDocument.recompute()

    myEx=App.ActiveDocument.addObject("Part::Extrusion","Extrude")
    myEx.Base = sk1
    myEx.Dir = (0,0,50)
    myEx.Solid = (True)
    myEx.TaperAngle = (0)
    myEx.Label = data[0]

    FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("Extrude").LineColor = (0.0,0.0,0.0)
    FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("Extrude").ShapeColor = (0.96,0.93,0.76)

    Gui.getDocument(App.ActiveDocument.Name).getObject("Sketch").Visibility=False
    App.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")

    App.ActiveDocument.saveAs(directory+data[0]+'.FCStd')
    __objs__=[]
    __objs__.append(FreeCAD.getDocument(App.ActiveDocument.Name).getObject("Extrude"))
    ImportGui.export(__objs__,directory+data[0]+'.step')
    Mesh.export(__objs__,directory+data[0]+'.stl')
    del __objs__
    App.closeDocument(App.ActiveDocument.Name)

print 'End'

 

 
 

