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
directory =LIBRARYPATH+'/Mechanical Parts/Profiles EN/EN10219 Sqare Hollow Sections/'
if not os.path.exists(directory):
    os.mkdir(directory)

Table = (
 	 ("Square hollow section 20x20x2 EN10219 S235JRH",	20,	20,	2.0, 	3,	2),
 	 ("Square hollow section 20x20x2.5 EN10219 S235JRH",	20,	20,	2.5,	3.75, 	2.5), 
 	 ("Square hollow section 25x25x2 EN10219 S235JRH",	25,	25,	2.0,	3,	2),
 	 ("Square hollow section 25x25x2.5 EN10219 S235JRH",	25,	25,	2.5, 	3.75, 	2.5), 
 	 ("Square hollow section 25x25x3 EN10219 S235JRH",	25,	25,	3.0,	4.5, 	3),
 	 ("Square hollow section 30x30x2 EN10219 S235JRH",	30,	30,	2.0,	3,	2),
 	 ("Square hollow section 30x30x2.5 EN10219 S235JRH",	30,	30,	2.5, 	3.75, 	2.5), 
 	 ("Square hollow section 30x30x3 EN10219 S235JRH",	30,	30,	3.0,	4.5, 	3),
 	 ("Square hollow section 40x40x2.5 EN10219 S235JRH",	40,	40,	2.5,	3.75, 	2.5 ),
 	 ("Square hollow section 40x40x3 EN10219 S235JRH",	40,	40,	3.0,	4.5,	3),
 	 ("Square hollow section 40x40x3.2 EN10219 S235JRH",	40,	40,	3.2,	4.8, 	3.2 ),
 	 ("Square hollow section 40x40x3.6 EN10219 S235JRH",	40,	40,	3.6,	5.4, 	3.6 ),
 	 ("Square hollow section 40x40x4 EN10219 S235JRH",	40,	40,	4.0,	6,	4),
 	 ("Square hollow section 40x40x5 EN10219 S235JRH",	40,	40,	5.0,	7.5, 	5),
 	 ("Square hollow section 50x50x2.5 EN10219 S235JRH",	50,	50,	2.5, 	3.75, 	2.5 ),
 	 ("Square hollow section 50x50x3 EN10219 S235JRH",	50,	50,	3.0, 	4.5, 	3),
 	 ("Square hollow section 50x50x3.2 EN10219 S235JRH",	50,	50,	3.2, 	4.8, 	3.2 ),
 	 ("Square hollow section 50x50x3.6 EN10219 S235JRH",	50,	50,	3.6, 	5.4, 	3.6 ),
 	 ("Square hollow section 50x50x4 EN10219 S235JRH",	50,	50,	4.0, 	6,	4),
 	 ("Square hollow section 50x50x5 EN10219 S235JRH",	50,	50,	5.0, 	7.5, 	5),
 	 ("Square hollow section 50x50x6 EN10219 S235JRH",	50,	50,	6.0, 	9,	6),
 	 ("Square hollow section 50x50x6.3 EN10219 S235JRH",	50,	50,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 60x60x2.5 EN10219 S235JRH",	60,	60,	2.5, 	3.75, 	2.5 ),
 	 ("Square hollow section 60x60x3 EN10219 S235JRH",	60,	60,	3.0, 	4.5, 	3),
 	 ("Square hollow section 60x60x3.2 EN10219 S235JRH",	60,	60,	3.2, 	4.8, 	3.2 ),
 	 ("Square hollow section 60x60x3.6 EN10219 S235JRH",	60,	60,	3.6, 	5.4, 	3.6 ),
 	 ("Square hollow section 60x60x4 EN10219 S235JRH",	60,	60,	4.0, 	6,	4),
 	 ("Square hollow section 60x60x5 EN10219 S235JRH",	60,	60,	5.0, 	7.5, 	5),
 	 ("Square hollow section 60x60x6 EN10219 S235JRH",	60,	60,	6.0, 	9,	6),
 	 ("Square hollow section 60x60x6.3 EN10219 S235JRH",	60,	60,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 60x60x8 EN10219 S235JRH",	60,	60,	8.0, 	12,	8),
 	 ("Square hollow section 70x70x3 EN10219 S235JRH",	70,	70,	3.0, 	4.5, 	3),
 	 ("Square hollow section 70x70x3.2 EN10219 S235JRH",	70,	70,	3.2, 	4.8,	3.2 ),
 	 ("Square hollow section 70x70x3.6 EN10219 S235JRH",	70,	70,	3.6, 	5.4, 	3.6 ),
 	 ("Square hollow section 70x70x4 EN10219 S235JRH",	70,	70,	4.0, 	6,	4),
 	 ("Square hollow section 70x70x5 EN10219 S235JRH",	70,	70,	5.0, 	7.5, 	5),
 	 ("Square hollow section 70x70x6 EN10219 S235JRH",	70,	70,	6.0, 	9,	6),
 	 ("Square hollow section 70x70x6.3 EN10219 S235JRH",	70,	70,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 70x70x8 EN10219 S235JRH",	70,	70,	8.0, 	12,	8),
 	 ("Square hollow section 80x80x3 EN10219 S235JRH",	80,	80,	3.0, 	4.5, 	3),
 	 ("Square hollow section 80x80x3.2 EN10219 S235JRH",	80,	80,	3.2, 	4.8, 	3.2 ),
 	 ("Square hollow section 80x80x3.6 EN10219 S235JRH",	80,	80,	3.6, 	5.4, 	3.6 ),
 	 ("Square hollow section 80x80x4 EN10219 S235JRH",	80,	80,	4.0, 	6,	4),
 	 ("Square hollow section 80x80x5 EN10219 S235JRH",	80,	80,	5.0, 	7.5, 	5),
 	 ("Square hollow section 80x80x6 EN10219 S235JRH",	80,	80,	6.0, 	9,	6),
 	 ("Square hollow section 80x80x6.3 EN10219 S235JRH",	80,	80,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 80x80x8 EN10219 S235JRH",	80,	80,	8.0, 	12,	8),
 	 ("Square hollow section 90x90x5 EN10219 S235JRH",	90,	90,	5.0, 	7.5, 	5),
 	 ("Square hollow section 90x90x6 EN10219 S235JRH",	90,	90,	6.0, 	9,	6),
 	 ("Square hollow section 90x90x6.3 EN10219 S235JRH",	90,	90,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 90x90x8 EN10219 S235JRH",	90,	90,	8.0, 	12,	8),
 	 ("Square hollow section 100x100x3.6 EN10219 S235JRH",	100,	100,	3.6, 	5.4, 	3.6 ),
 	 ("Square hollow section 100x100x4 EN10219 S235JRH",	100,	100,	4.0, 	6,	4),
 	 ("Square hollow section 100x100x5 EN10219 S235JRH",	100,	100,	5.0, 	7.5, 	5),
 	 ("Square hollow section 100x100x6 EN10219 S235JRH",	100,	100,	6.0, 	9,	6),
 	 ("Square hollow section 100x100x6.3 EN10219 S235JRH",	100,	100,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 100x100x8 EN10219 S235JRH",	100,	100,	8.0, 	12,	8),
 	 ("Square hollow section 100x100x10 EN10219 S235JRH",	100,	100,	10.0, 	15,	10),
 	 ("Square hollow section 120x120x4 EN10219 S235JRH",	120,	120,	4.0, 	6,	4),
 	 ("Square hollow section 120x120x5 EN10219 S235JRH",	120,	120,	5.0, 	7.5, 	5),
 	 ("Square hollow section 120x120x6 EN10219 S235JRH",	120,	120,	6.0, 	9,	6),
 	 ("Square hollow section 120x120x6.3 EN10219 S235JRH",	120,	120,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 120x120x8 EN10219 S235JRH",	120,	120,	8.0, 	12,	8),
 	 ("Square hollow section 120x120x10 EN10219 S235JRH",	120,	120,	10.0, 	15,	10),
 	 ("Square hollow section 120x120x12 EN10219 S235JRH",	120,	120,	12.0, 	18,	12),
 	 ("Square hollow section 120x120x12.5 EN10219 S235JRH",	120,	120,	12.5, 	18.75, 	12.5), 
 	 ("Square hollow section 140x140x5 EN10219 S235JRH",	140,	140,	5.0, 	7.5, 	5),
 	 ("Square hollow section 140x140x6 EN10219 S235JRH",	140,	140,	6.0, 	9,	6),
 	 ("Square hollow section 140x140x6.3 EN10219 S235JRH",	140,	140,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 140x140x8 EN10219 S235JRH",	140,	140,	8.0, 	12,	8),
 	 ("Square hollow section 140x140x10 EN10219 S235JRH",	140,	140,	10.0, 	15,	10),
 	 ("Square hollow section 140x140x12 EN10219 S235JRH",	140,	140,	12.0, 	18,	12),
 	 ("Square hollow section 140x140x12.5 EN10219 S235JRH",	140,	140,	12.5, 	18.75, 	12.5), 
 	 ("Square hollow section 150x150x5 EN10219 S235JRH",	150,	150,	5.0, 	7.5, 	5),
 	 ("Square hollow section 150x150x6 EN10219 S235JRH",	150,	150,	6.0, 	9,	6),
 	 ("Square hollow section 150x150x6.3 EN10219 S235JRH",	150,	150,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 150x150x8 EN10219 S235JRH",	150,	150,	8.0, 	12,	8),
 	 ("Square hollow section 150x150x10 EN10219 S235JRH",	150,	150,	10.0, 	15,	10),
 	 ("Square hollow section 150x150x12 EN10219 S235JRH",	150,	150,	12.0, 	18,	12),
 	 ("Square hollow section 150x150x12.5 EN10219 S235JRH",	150,	150,	12.5, 	18.75, 	12.5), 
 	 ("Square hollow section 150x150x16 EN10219 S235JRH",	150,	150,	16.0, 	24,	16),
 	 ("Square hollow section 160x160x5 EN10219 S235JRH",	160,	160,	5.0, 	7.5, 	5),
 	 ("Square hollow section 160x160x6 EN10219 S235JRH",	160,	160,	6.0, 	9,	6),
 	 ("Square hollow section 160x160x6.3 EN10219 S235JRH",	160,	160,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 160x160x8 EN10219 S235JRH",	160,	160,	8.0, 	12,	8),
 	 ("Square hollow section 160x160x10 EN10219 S235JRH",	160,	160,	10.0, 	15,	10),
 	 ("Square hollow section 160x160x12 EN10219 S235JRH",	160,	160,	12.0, 	18,	12),
 	 ("Square hollow section 160x160x12.5 EN10219 S235JRH",	160,	160,	12.5, 	18.75, 	12.5 ),
 	 ("Square hollow section 160x160x16 EN10219 S235JRH",	160,	160,	16.0, 	24,	16),
 	 ("Square hollow section 180x180x5 EN10219 S235JRH",	180,	180,	5.0, 	7.5, 	5),
 	 ("Square hollow section 180x180x6 EN10219 S235JRH",	180,	180,	6.0, 	9,	6),
 	 ("Square hollow section 180x180x6.3 EN10219 S235JRH",	180,	180,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 180x180x8 EN10219 S235JRH",	180,	180,	8.0, 	12,	8),
 	 ("Square hollow section 180x180x10 EN10219 S235JRH",	180,	180,	10.0, 	15,	10),
 	 ("Square hollow section 180x180x12 EN10219 S235JRH",	180,	180,	12.0, 	18,	12),
 	 ("Square hollow section 180x180x12.5 EN10219 S235JRH",	180,	180,	12.5, 	18.75, 	12.5 ),
 	 ("Square hollow section 180x180x16 EN10219 S235JRH",	180,	180,	16.0, 	24,	16),
 	 ("Square hollow section 200x200x5 EN10219 S235JRH",	200,	200,	5.0, 	7.5, 	5),
 	 ("Square hollow section 200x200x6 EN10219 S235JRH",	200,	200,	6.0, 	9,	6),
 	 ("Square hollow section 200x200x6.3 EN10219 S235JRH",	200,	200,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 200x200x8 EN10219 S235JRH",	200,	200,	8.0, 	12,	8),
 	 ("Square hollow section 200x200x10 EN10219 S235JRH",	200,	200,	10.0, 	15,	10),
 	 ("Square hollow section 200x200x12 EN10219 S235JRH",	200,	200,	12.0, 	18,	12),
 	 ("Square hollow section 200x200x12.5 EN10219 S235JRH",	200,	200,	12.5, 	18.75, 	12.5 ),
 	 ("Square hollow section 200x200x16 EN10219 S235JRH",	200,	200,	16.0, 	24,	16),
 	 ("Square hollow section 220x220x6 EN10219 S235JRH",	220,	220,	6.0, 	9,	6),
 	 ("Square hollow section 220x220x6.3 EN10219 S235JRH",	220,	220,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 220x220x8 EN10219 S235JRH",	220,	220,	8.0, 	12,	8),
 	 ("Square hollow section 220x220x10 EN10219 S235JRH",	220,	220,	10.0, 	15,	10),
 	 ("Square hollow section 220x220x12 EN10219 S235JRH",	220,	220,	12.0, 	18,	12),
 	 ("Square hollow section 220x220x12.5 EN10219 S235JRH",	220,	220,	12.5, 	18.75, 	12.5), 
 	 ("Square hollow section 220x220x16 EN10219 S235JRH",	220,	220,	16.0, 	24,	16),
 	 ("Square hollow section 250x250x5 EN10219 S235JRH",	250,	250,	5.0, 	7.5, 	5),
 	 ("Square hollow section 250x250x6 EN10219 S235JRH",	250,	250,	6.0, 	9,	6),
 	 ("Square hollow section 250x250x6.3 EN10219 S235JRH",	250,	250,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 250x250x8 EN10219 S235JRH",	250,	250,	8.0, 	12,	8),
 	 ("Square hollow section 250x250x10 EN10219 S235JRH",	250,	250,	10.0, 	15,	10),
 	 ("Square hollow section 250x250x12 EN10219 S235JRH",	250,	250,	12.0, 	18,	12),
 	 ("Square hollow section 250x250x12.5 EN10219 S235JRH",	250,	250,	12.5, 	18.75, 	12.5), 
 	 ("Square hollow section 250x250x16 EN10219 S235JRH",	250,	250,	16.0, 	24,	16),
 	 ("Square hollow section 260x260x6 EN10219 S235JRH",	260,	260,	6.0, 	9,	6),
 	 ("Square hollow section 260x260x6.3 EN10219 S235JRH",	260,	260,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 260x260x8 EN10219 S235JRH",	260,	260,	8.0, 	12,	8),
 	 ("Square hollow section 260x260x10 EN10219 S235JRH",	260,	260,	10.0, 	15,	10),
 	 ("Square hollow section 260x260x12 EN10219 S235JRH",	260,	260,	12.0, 	18,	12),
 	 ("Square hollow section 260x260x12.5 EN10219 S235JRH",	260,	260,	12.5, 	18.75, 	12.5 ),
 	 ("Square hollow section 260x260x16 EN10219 S235JRH",	260,	260,	16.0, 	24,	16),
 	 ("Square hollow section 300x300x6 EN10219 S235JRH",	300,	300,	6.0, 	9,	6),
 	 ("Square hollow section 300x300x6.3 EN10219 S235JRH",	300,	300,	6.3, 	9.45, 	6.3 ),
 	 ("Square hollow section 300x300x8 EN10219 S235JRH",	300,	300,	8.0, 	12,	8),
 	 ("Square hollow section 300x300x10 EN10219 S235JRH",	300,	300,	10.0, 	15,	10),
 	 ("Square hollow section 300x300x12 EN10219 S235JRH",	300,	300,	12.0, 	18,	12),
 	 ("Square hollow section 300x300x12.5 EN10219 S235JRH",	300,	300,	12.5, 	18.75, 	12.5 ),
 	 ("Square hollow section 300x300x16 EN10219 S235JRH",	300,	300,	16.0, 	24,	16),
 	 ("Square hollow section 350x350x8 EN10219 S235JRH",	350,	350,	8.0, 	12,	8),
 	 ("Square hollow section 350x350x10 EN10219 S235JRH",	350,	350,	10.0, 	15,	10),
 	 ("Square hollow section 350x350x12 EN10219 S235JRH",	350,	350,	12.0, 	18,	12),
 	 ("Square hollow section 350x350x12.5 EN10219 S235JRH",	350,	350,	12.5, 	18.75, 	12.5 ),
 	 ("Square hollow section 350x350x16 EN10219 S235JRH",	350,	350,	16.0, 	24,	16),
 	 ("Square hollow section 400x400x8 EN10219 S235JRH",	400,	400,	8.0, 	12,	8),
 	 ("Square hollow section 400x400x10 EN10219 S235JRH",	400,	400,	10.0, 	15,	10),
 	 ("Square hollow section 400x400x12 EN10219 S235JRH",	400,	400,	12.0, 	18,	12),
 	 ("Square hollow section 400x400x12.5 EN10219 S235JRH",	400,	400,	12.5, 	18.75, 	12.5 ),
 	 ("Square hollow section 400x400x16 EN10219 S235JRH",	400,	400,	16.0, 	24,	16),
 	 ("Square hollow section 400x400x20 EN10219 S235JRH",	400,	400,	20.0, 	30,	20))





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

 

 
 

