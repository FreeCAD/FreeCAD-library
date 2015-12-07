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
directory =LIBRARYPATH+'/Mechanical Parts/Profiles EN/EN10058 Flat steel bars/'
if not os.path.exists(directory):
    os.mkdir(directory)


Table = (("Flat Bar 20x3 EN10058 S235JR", 20, 3),
         ("Flat Bar 20x4 EN10058 S235JR", 20, 4),
         ("Flat Bar 20x5 EN10058 S235JR", 20, 5),
         ("Flat Bar 20x6 EN10058 S235JR", 20, 6),
         ("Flat Bar 20x8 EN10058 S235JR", 20, 8),
         ("Flat Bar 20x10 EN10058 S235JR", 20, 10),
         ("Flat Bar 20x12 EN10058 S235JR", 20, 12),
         ("Flat Bar 20x15 EN10058 S235JR", 20, 15),
         ("Flat Bar 25x3 EN10058 S235JR", 25, 3),
         ("Flat Bar 25x4 EN10058 S235JR", 25, 4),
         ("Flat Bar 25x5 EN10058 S235JR", 25, 5),
         ("Flat Bar 25x6 EN10058 S235JR", 25, 6),
         ("Flat Bar 25x8 EN10058 S235JR", 25, 8),
         ("Flat Bar 25x10 EN10058 S235JR", 25, 10),
         ("Flat Bar 25x15 EN10058 S235JR", 25, 15),
         ("Flat Bar 25x20 EN10058 S235JR", 25, 20),
         ("Flat Bar 30x3 EN10058 S235JR", 30, 3),
         ("Flat Bar 30x4 EN10058 S235JR", 30, 4),
         ("Flat Bar 30x5 EN10058 S235JR", 30, 5),
         ("Flat Bar 30x6 EN10058 S235JR", 30, 6),
         ("Flat Bar 30x8 EN10058 S235JR", 30, 8),
         ("Flat Bar 30x10 EN10058 S235JR", 30, 10),
         ("Flat Bar 30x12 EN10058 S235JR", 30, 12),
         ("Flat Bar 30x15 EN10058 S235JR", 30, 15),
         ("Flat Bar 30x16 EN10058 S235JR", 30, 16),
         ("Flat Bar 30x20 EN10058 S235JR", 30, 20),
         ("Flat Bar 30x25 EN10058 S235JR", 30, 25),
         ("Flat Bar 35x5 EN10058 S235JR", 35, 5),
         ("Flat Bar 35x6 EN10058 S235JR", 35, 6),
         ("Flat Bar 35x8 EN10058 S235JR", 35, 8),
         ("Flat Bar 35x10 EN10058 S235JR", 35, 10),
         ("Flat Bar 35x15 EN10058 S235JR", 35, 15),
         ("Flat Bar 35x20 EN10058 S235JR", 35, 20),
         ("Flat Bar 40x4 EN10058 S235JR", 40, 4),
         ("Flat Bar 40x5 EN10058 S235JR", 40, 5),
         ("Flat Bar 40x6 EN10058 S235JR", 40, 6),
         ("Flat Bar 40x8 EN10058 S235JR", 40, 8),
         ("Flat Bar 40x10 EN10058 S235JR", 40, 10),
         ("Flat Bar 40x12 EN10058 S235JR", 40, 12),
         ("Flat Bar 40x15 EN10058 S235JR", 40, 15),
         ("Flat Bar 40x16 EN10058 S235JR", 40, 16),
         ("Flat Bar 40x20 EN10058 S235JR", 40, 20),
         ("Flat Bar 40x25 EN10058 S235JR", 40, 25),
         ("Flat Bar 40x30 EN10058 S235JR", 40, 30),
         ("Flat Bar 45x5 EN10058 S235JR", 45, 5),
         ("Flat Bar 45x6 EN10058 S235JR", 45, 6),
         ("Flat Bar 45x8 EN10058 S235JR", 45, 8),
         ("Flat Bar 45x10 EN10058 S235JR", 45, 10),
         ("Flat Bar 45x12 EN10058 S235JR", 45, 12),
         ("Flat Bar 45x15 EN10058 S235JR", 45, 15),
         ("Flat Bar 45x20 EN10058 S235JR", 45, 20),
         ("Flat Bar 45x25 EN10058 S235JR", 45, 25),
         ("Flat Bar 45x30 EN10058 S235JR", 45, 30),
         ("Flat Bar 50x3 EN10058 S235JR", 50, 3),
         ("Flat Bar 50x4 EN10058 S235JR", 50, 4),
         ("Flat Bar 50x5 EN10058 S235JR", 50, 5),
         ("Flat Bar 50x6 EN10058 S235JR", 50, 6),
         ("Flat Bar 50x8 EN10058 S235JR", 50, 8),
         ("Flat Bar 50x10 EN10058 S235JR", 50, 10),
         ("Flat Bar 50x12 EN10058 S235JR", 50, 12),
         ("Flat Bar 50x15 EN10058 S235JR", 50, 15),
         ("Flat Bar 50x16 EN10058 S235JR", 50, 16),
         ("Flat Bar 50x20 EN10058 S235JR", 50, 20),
         ("Flat Bar 50x25 EN10058 S235JR", 50, 25),
         ("Flat Bar 50x30 EN10058 S235JR", 50, 30),
         ("Flat Bar 50x40 EN10058 S235JR", 50, 40),
         ("Flat Bar 55x5 EN10058 S235JR", 55, 5),
         ("Flat Bar 55x10 EN10058 S235JR", 55, 10),
         ("Flat Bar 60x3 EN10058 S235JR", 60, 3),
         ("Flat Bar 60x4 EN10058 S235JR", 60, 4),
         ("Flat Bar 60x5 EN10058 S235JR", 60, 5),
         ("Flat Bar 60x6 EN10058 S235JR", 60, 6),
         ("Flat Bar 60x8 EN10058 S235JR", 60, 8),
         ("Flat Bar 60x10 EN10058 S235JR", 60, 10),
         ("Flat Bar 60x12 EN10058 S235JR", 60, 12),
         ("Flat Bar 60x15 EN10058 S235JR", 60, 15),
         ("Flat Bar 60x16 EN10058 S235JR", 60, 16),
         ("Flat Bar 60x20 EN10058 S235JR", 60, 20),
         ("Flat Bar 60x25 EN10058 S235JR", 60, 25),
         ("Flat Bar 60x30 EN10058 S235JR", 60, 30),
         ("Flat Bar 60x40 EN10058 S235JR", 60, 40),
         ("Flat Bar 60x50 EN10058 S235JR", 60, 50),
         ("Flat Bar 65x16 EN10058 S235JR", 65, 16),
         ("Flat Bar 65x40 EN10058 S235JR", 65, 40),
         ("Flat Bar 70x5 EN10058 S235JR", 70, 5),
         ("Flat Bar 70x6 EN10058 S235JR", 70, 6),
         ("Flat Bar 70x8 EN10058 S235JR", 70, 8),
         ("Flat Bar 70x10 EN10058 S235JR", 70, 10),
         ("Flat Bar 70x12 EN10058 S235JR", 70, 12),
         ("Flat Bar 70x15 EN10058 S235JR", 70, 15),
         ("Flat Bar 70x16 EN10058 S235JR", 70, 16),
         ("Flat Bar 70x20 EN10058 S235JR", 70, 20),
         ("Flat Bar 70x25 EN10058 S235JR", 70, 25),
         ("Flat Bar 70x30 EN10058 S235JR", 70, 30),
         ("Flat Bar 70x40 EN10058 S235JR", 70, 40),
         ("Flat Bar 70x50 EN10058 S235JR", 70, 50),
         ("Flat Bar 80x5 EN10058 S235JR", 80, 5),
         ("Flat Bar 80x6 EN10058 S235JR", 80, 6),
         ("Flat Bar 80x8 EN10058 S235JR", 80, 8),
         ("Flat Bar 80x10 EN10058 S235JR", 80, 10),
         ("Flat Bar 80x12 EN10058 S235JR", 80, 12),
         ("Flat Bar 80x15 EN10058 S235JR", 80, 15),
         ("Flat Bar 80x16 EN10058 S235JR", 80, 16),
         ("Flat Bar 80x20 EN10058 S235JR", 80, 20),
         ("Flat Bar 80x25 EN10058 S235JR", 80, 25),
         ("Flat Bar 80x30 EN10058 S235JR", 80, 30),
         ("Flat Bar 80x40 EN10058 S235JR", 80, 40),
         ("Flat Bar 80x50 EN10058 S235JR", 80, 50),
         ("Flat Bar 80x60 EN10058 S235JR", 80, 60),
         ("Flat Bar 90x5 EN10058 S235JR", 90, 5),
         ("Flat Bar 90x6 EN10058 S235JR", 90, 6),
         ("Flat Bar 90x8 EN10058 S235JR", 90, 8),
         ("Flat Bar 90x10 EN10058 S235JR", 90, 10),
         ("Flat Bar 90x12 EN10058 S235JR", 90, 12),
         ("Flat Bar 90x15 EN10058 S235JR", 90, 15),
         ("Flat Bar 90x16 EN10058 S235JR", 90, 16),
         ("Flat Bar 90x20 EN10058 S235JR", 90, 20),
         ("Flat Bar 90x25 EN10058 S235JR", 90, 25),
         ("Flat Bar 90x30 EN10058 S235JR", 90, 30),
         ("Flat Bar 90x40 EN10058 S235JR", 90, 40),
         ("Flat Bar 90x50 EN10058 S235JR", 90, 50),
         ("Flat Bar 90x60 EN10058 S235JR", 90, 60),
         ("Flat Bar 100x5 EN10058 S235JR", 100, 5),
         ("Flat Bar 100x6 EN10058 S235JR", 100, 6),
         ("Flat Bar 100x8 EN10058 S235JR", 100, 8),
         ("Flat Bar 100x10 EN10058 S235JR", 100, 10),
         ("Flat Bar 100x12 EN10058 S235JR", 100, 12),
         ("Flat Bar 100x15 EN10058 S235JR", 100, 15),
         ("Flat Bar 100x16 EN10058 S235JR", 100, 16),
         ("Flat Bar 100x18 EN10058 S235JR", 100, 18),
         ("Flat Bar 100x20 EN10058 S235JR", 100, 20),
         ("Flat Bar 100x25 EN10058 S235JR", 100, 25),
         ("Flat Bar 100x30 EN10058 S235JR", 100, 30),
         ("Flat Bar 100x40 EN10058 S235JR", 100, 40),
         ("Flat Bar 100x50 EN10058 S235JR", 100, 50),
         ("Flat Bar 100x60 EN10058 S235JR", 100, 60),
         ("Flat Bar 110x6 EN10058 S235JR", 110, 6),
         ("Flat Bar 110x8 EN10058 S235JR", 110, 8),
         ("Flat Bar 110x10 EN10058 S235JR", 110, 10),
         ("Flat Bar 110x12 EN10058 S235JR", 110, 12),
         ("Flat Bar 110x15 EN10058 S235JR", 110, 15),
         ("Flat Bar 110x20 EN10058 S235JR", 110, 20),
         ("Flat Bar 110x25 EN10058 S235JR", 110, 25),
         ("Flat Bar 110x30 EN10058 S235JR", 110, 30),
         ("Flat Bar 110x40 EN10058 S235JR", 110, 40),
         ("Flat Bar 110x50 EN10058 S235JR", 110, 50),
         ("Flat Bar 120x5 EN10058 S235JR", 120, 5),
         ("Flat Bar 120x6 EN10058 S235JR", 120, 6),
         ("Flat Bar 120x8 EN10058 S235JR", 120, 8),
         ("Flat Bar 120x10 EN10058 S235JR", 120, 10),
         ("Flat Bar 120x12 EN10058 S235JR", 120, 12),
         ("Flat Bar 120x15 EN10058 S235JR", 120, 15),
         ("Flat Bar 120x16 EN10058 S235JR", 120, 16),
         ("Flat Bar 120x20 EN10058 S235JR", 120, 20),
         ("Flat Bar 120x25 EN10058 S235JR", 120, 25),
         ("Flat Bar 120x30 EN10058 S235JR", 120, 30),
         ("Flat Bar 120x40 EN10058 S235JR", 120, 40),
         ("Flat Bar 120x50 EN10058 S235JR", 120, 50),
         ("Flat Bar 120x60 EN10058 S235JR", 120, 60),
         ("Flat Bar 125x30 EN10058 S235JR", 125, 30),
         ("Flat Bar 130x6 EN10058 S235JR", 130, 6),
         ("Flat Bar 130x8 EN10058 S235JR", 130, 8),
         ("Flat Bar 130x10 EN10058 S235JR", 130, 10),
         ("Flat Bar 130x12 EN10058 S235JR", 130, 12),
         ("Flat Bar 130x15 EN10058 S235JR", 130, 15),
         ("Flat Bar 130x20 EN10058 S235JR", 130, 20),
         ("Flat Bar 130x25 EN10058 S235JR", 130, 25),
         ("Flat Bar 130x30 EN10058 S235JR", 130, 30),
         ("Flat Bar 130x40 EN10058 S235JR", 130, 40),
         ("Flat Bar 130x50 EN10058 S235JR", 130, 50),
         ("Flat Bar 130x60 EN10058 S235JR", 130, 60),
         ("Flat Bar 130x70 EN10058 S235JR", 130, 70),
         ("Flat Bar 130x80 EN10058 S235JR", 130, 80),
         ("Flat Bar 140x5 EN10058 S235JR", 140, 5),
         ("Flat Bar 140x6 EN10058 S235JR", 140, 6),
         ("Flat Bar 140x8 EN10058 S235JR", 140, 8),
         ("Flat Bar 140x10 EN10058 S235JR", 140, 10),
         ("Flat Bar 140x12 EN10058 S235JR", 140, 12),
         ("Flat Bar 140x15 EN10058 S235JR", 140, 15),
         ("Flat Bar 140x16 EN10058 S235JR", 140, 16),
         ("Flat Bar 140x20 EN10058 S235JR", 140, 20),
         ("Flat Bar 140x25 EN10058 S235JR", 140, 25),
         ("Flat Bar 140x30 EN10058 S235JR", 140, 30),
         ("Flat Bar 140x40 EN10058 S235JR", 140, 40),
         ("Flat Bar 140x50 EN10058 S235JR", 140, 50),
         ("Flat Bar 150x5 EN10058 S235JR", 150, 5),
         ("Flat Bar 150x6 EN10058 S235JR", 150, 6),
         ("Flat Bar 150x8 EN10058 S235JR", 150, 8),
         ("Flat Bar 150x10 EN10058 S235JR", 150, 10),
         ("Flat Bar 150x12 EN10058 S235JR", 150, 12),
         ("Flat Bar 150x15 EN10058 S235JR", 150, 15),
         ("Flat Bar 150x16 EN10058 S235JR", 150, 16),
         ("Flat Bar 150x20 EN10058 S235JR", 150, 20),
         ("Flat Bar 150x25 EN10058 S235JR", 150, 25),
         ("Flat Bar 150x30 EN10058 S235JR", 150, 30),
         ("Flat Bar 150x40 EN10058 S235JR", 150, 40),
         ("Flat Bar 150x50 EN10058 S235JR", 150, 50),
         ("Flat Bar 150x60 EN10058 S235JR", 150, 60),
         ("Flat Bar 160x8 EN10058 S235JR", 160, 8),
         ("Flat Bar 160x10 EN10058 S235JR", 160, 10),
         ("Flat Bar 160x12 EN10058 S235JR", 160, 12),
         ("Flat Bar 160x15 EN10058 S235JR", 160, 15),
         ("Flat Bar 160x20 EN10058 S235JR", 160, 20),
         ("Flat Bar 160x25 EN10058 S235JR", 160, 25),
         ("Flat Bar 160x30 EN10058 S235JR", 160, 30),
         ("Flat Bar 160x40 EN10058 S235JR", 160, 40),
         ("Flat Bar 160x50 EN10058 S235JR", 160, 50),
         ("Flat Bar 160x60 EN10058 S235JR", 160, 60),
         ("Flat Bar 180x8 EN10058 S235JR", 180, 8),
         ("Flat Bar 180x10 EN10058 S235JR", 180, 10),
         ("Flat Bar 180x12 EN10058 S235JR", 180, 12),
         ("Flat Bar 180x15 EN10058 S235JR", 180, 15),
         ("Flat Bar 180x20 EN10058 S235JR", 180, 20),
         ("Flat Bar 180x25 EN10058 S235JR", 180, 25),
         ("Flat Bar 180x30 EN10058 S235JR", 180, 30),
         ("Flat Bar 180x40 EN10058 S235JR", 180, 40),
         ("Flat Bar 180x50 EN10058 S235JR", 180, 50),
         ("Flat Bar 200x8 EN10058 S235JR", 200, 8),
         ("Flat Bar 200x10 EN10058 S235JR", 200, 10),
         ("Flat Bar 200x12 EN10058 S235JR", 200, 12),
         ("Flat Bar 200x15 EN10058 S235JR", 200, 15),
         ("Flat Bar 200x20 EN10058 S235JR", 200, 20),
         ("Flat Bar 200x25 EN10058 S235JR", 200, 25),
         ("Flat Bar 200x30 EN10058 S235JR", 200, 30)) 

for data in Table:
    print data[0]
    doc=FreeCAD.newDocument("Bar")
    sk1=doc.addObject('Sketcher::SketchObject','Sketch')
    sk1.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation  (0.000000,0.000000,0.000000,1.000000))
    sk1.addGeometry(Part.Line(App.Vector(-20.000000,-10.000000,0),App.Vector(20.000000,-10.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(20.000000,-10.000000,0),App.Vector(20.000000,10.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(20.000000,10.000000,0),App.Vector(-20.000000,10.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(-20.000000,10.000000,0),App.Vector(-20.000000,-10.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',0)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',2)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',1)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',3)) 
    sk1.addConstraint(Sketcher.Constraint('Symmetric',1,2,2,2,-2)) 
    sk1.addConstraint(Sketcher.Constraint('Symmetric',0,2,1,2,-1)) 
    sk1.addConstraint(Sketcher.Constraint('DistanceY',1,20.000000)) 
    sk1.setDatum(10,App.Units.Quantity(str(data[2])+' mm'))
    sk1.addConstraint(Sketcher.Constraint('DistanceX',0,40.000000)) 
    sk1.setDatum(11,App.Units.Quantity(str(data[1])+' mm'))

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

 

 
 

