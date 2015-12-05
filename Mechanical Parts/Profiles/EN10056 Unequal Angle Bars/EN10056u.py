# -*- coding:utf-8 -*-
import FreeCAD, FreeCADGui, Part, Draft, math, MeshPart, Mesh, Drawing
from PyQt4 import QtGui,QtCore
from FreeCAD import Base
from FreeCAD import Vector
import ImportGui
import Mesh

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

Table = (
 	 ("Angle Bar 30x20x3 EN10056 S235JR", 30, 20, 3, 3.5, 2),
 	 ("Angle Bar 30x20x4 EN10056 S235JR", 30, 20, 4, 3.5, 2),
 	 ("Angle Bar 40x20x3 EN10056 S235JR", 40, 20, 3, 3.5, 2),
 	 ("Angle Bar 40x20x4 EN10056 S235JR", 40, 20, 4, 3.5, 2),
 	 ("Angle Bar 40x25x3 EN10056 S235JR", 40, 25, 3, 4, 2),
 	 ("Angle Bar 40x25x4 EN10056 S235JR", 40, 25, 4, 4, 2),
 	 ("Angle Bar 40x25x5 EN10056 S235JR", 40, 25, 5, 4, 2),
 	 ("Angle Bar 45x30x3 EN10056 S235JR", 45, 30, 3, 4.5, 2),
 	 ("Angle Bar 45x30x4 EN10056 S235JR", 45, 30, 4, 4.5, 2),
 	 ("Angle Bar 45x30x5 EN10056 S235JR", 45, 30, 5, 4.5, 2),
 	 ("Angle Bar 50x30x4 EN10056 S235JR", 50, 30, 4, 4.5, 2),
 	 ("Angle Bar 50x30x5 EN10056 S235JR", 50, 30, 5, 4.5, 2),
 	 ("Angle Bar 50x40x4 EN10056 S235JR", 50, 40, 4, 4, 2),
 	 ("Angle Bar 50x40x5 EN10056 S235JR", 50, 40, 5, 4, 2),
 	 ("Angle Bar 60x30x5 EN10056 S235JR", 60, 30, 5, 6, 3),
 	 ("Angle Bar 60x40x5 EN10056 S235JR", 60, 40, 5, 6, 3),
 	 ("Angle Bar 60x40x6 EN10056 S235JR", 60, 40, 6, 6, 3),
 	 ("Angle Bar 60x40x7 EN10056 S235JR", 60, 40, 7, 6, 3),
 	 ("Angle Bar 65x50x5 EN10056 S235JR", 65, 50, 5, 6.5, 3.5),
 	 ("Angle Bar 65x50x6 EN10056 S235JR", 65, 50, 6, 6.5, 3.5),
 	 ("Angle Bar 65x50x7 EN10056 S235JR", 65, 50, 7, 6.5, 3.5),
 	 ("Angle Bar 65x50x8 EN10056 S235JR", 65, 50, 8, 6.5, 3.5),
 	 ("Angle Bar 65x50x9 EN10056 S235JR", 65, 50, 9, 6.5, 3.5),
 	 ("Angle Bar 70x50x6 EN10056 S235JR", 70, 50, 6, 6, 3),
 	 ("Angle Bar 70x50x5 EN10056 S235JR", 70, 50, 5, 6, 3),
 	 ("Angle Bar 70x50x6 EN10056 S235JR", 70, 50, 6, 6, 3),
 	 ("Angle Bar 70x50x7 EN10056 S235JR", 70, 50, 7, 6.5, 3.5),
 	 ("Angle Bar 70x50x8 EN10056 S235JR", 70, 50, 8, 6.5, 3.5),
 	 ("Angle Bar 70x50x9 EN10056 S235JR", 70, 50, 9, 6.5, 3.5),
 	 ("Angle Bar 80x40x6 EN10056 S235JR", 80, 40, 6, 7, 3.5),
 	 ("Angle Bar 80x40x8 EN10056 S235JR", 80, 40, 8, 7, 3.5),
 	 ("Angle Bar 80x60x6 EN10056 S235JR", 80, 60, 6, 8, 4),
 	 ("Angle Bar 80x60x7 EN10056 S235JR", 80, 60, 7, 8, 4),
 	 ("Angle Bar 80x60x8 EN10056 S235JR", 80, 60, 8, 8, 4),
 	 ("Angle Bar 80x65x8 EN10056 S235JR", 80, 65, 8, 8, 4),
 	 ("Angle Bar 80x65x10 EN10056 S235JR", 80, 65, 10, 8, 4),
 	 ("Angle Bar 90x60x6 EN10056 S235JR", 90, 60, 6, 7, 3.5),
 	 ("Angle Bar 90x60x8 EN10056 S235JR", 90, 60, 8, 7, 3.5),
 	 ("Angle Bar 100x50x6 EN10056 S235JR", 100, 50, 6, 9, 4.5),
 	 ("Angle Bar 100x50x8 EN10056 S235JR", 100, 50, 8, 9, 4.5),
 	 ("Angle Bar 100x50x10 EN10056 S235JR", 100, 50, 10, 9, 4.5),
 	 ("Angle Bar 100x65x7 EN10056 S235JR", 100, 65, 7, 10, 5),
 	 ("Angle Bar 100x65x8 EN10056 S235JR", 100, 65, 8, 10, 5),
 	 ("Angle Bar 100x65x9 EN10056 S235JR", 100, 65, 9, 10, 5),
 	 ("Angle Bar 100x65x10 EN10056 S235JR", 100, 65, 10, 10, 5),
 	 ("Angle Bar 100x65x11 EN10056 S235JR", 100, 65, 11, 10, 5),
 	 ("Angle Bar 100x65x12 EN10056 S235JR", 100, 65, 12, 10, 5),
 	 ("Angle Bar 100x75x7 EN10056 S235JR", 100, 75, 7, 10, 5),
 	 ("Angle Bar 100x75x9 EN10056 S235JR", 100, 75, 9, 10, 5),
 	 ("Angle Bar 100x75x11 EN10056 S235JR", 100, 75, 11, 10, 5),
 	 ("Angle Bar 110x70x10 EN10056 S235JR", 110, 70, 10, 10, 5),
 	 ("Angle Bar 110x70x12 EN10056 S235JR", 110, 70, 12, 10, 5),
 	 ("Angle Bar 120x80x8 EN10056 S235JR", 120, 80, 8, 11, 5.5),
 	 ("Angle Bar 120x80x10 EN10056 S235JR", 120, 80, 10, 11, 5.5),
 	 ("Angle Bar 120x80x12 EN10056 S235JR", 120, 80, 12, 11, 5.5),
 	 ("Angle Bar 130x65x8 EN10056 S235JR", 130, 65, 8, 11, 5.5),
 	 ("Angle Bar 130x65x10 EN10056 S235JR", 130, 65, 10, 11, 5.5),
 	 ("Angle Bar 130x65x12 EN10056 S235JR", 130, 65, 12, 11, 5.5),
 	 ("Angle Bar 130x90x10 EN10056 S235JR", 130, 90, 10, 11, 5),
 	 ("Angle Bar 130x90x12 EN10056 S235JR", 130, 90, 12, 12, 6),
 	 ("Angle Bar 130x90x14 EN10056 S235JR", 130, 90, 14, 11, 5),
 	 ("Angle Bar 140x90x8 EN10056 S235JR", 140, 90, 8, 11, 5.5),
 	 ("Angle Bar 140x90x10 EN10056 S235JR", 140, 90, 10, 11, 5.5),
 	 ("Angle Bar 140x90x12 EN10056 S235JR", 140, 90, 12, 11, 5.5),
 	 ("Angle Bar 140x90x14 EN10056 S235JR", 140, 90, 14, 11, 5.5),
 	 ("Angle Bar 150x75x9 EN10056 S235JR", 150, 75, 9, 10, 5.5),
 	 ("Angle Bar 150x75x11 EN10056 S235JR", 150, 75, 11, 10.5, 5.5),
 	 ("Angle Bar 150x100x10 EN10056 S235JR", 150, 100, 10, 13, 6.5),
 	 ("Angle Bar 150x100x12 EN10056 S235JR", 150, 100, 12, 13, 6.5),
 	 ("Angle Bar 150x100x14 EN10056 S235JR", 150, 100, 14, 13, 6.5),
 	 ("Angle Bar 160x100x10 EN10056 S235JR", 160, 100, 10, 13, 6.5),
 	 ("Angle Bar 160x100x12 EN10056 S235JR", 160, 100, 12, 13, 6.5),
 	 ("Angle Bar 160x100x14 EN10056 S235JR", 160, 100, 14, 13, 6.5),
 	 ("Angle Bar 180x90x10 EN10056 S235JR", 180, 90, 10, 14, 7),
 	 ("Angle Bar 180x90x12 EN10056 S235JR", 180, 90, 12, 14, 7),
 	 ("Angle Bar 200x100x10 EN10056 S235JR", 200, 100, 10, 15, 7.5),
 	 ("Angle Bar 200x100x12 EN10056 S235JR", 200, 100, 12, 15, 7.5),
 	 ("Angle Bar 200x100x14 EN10056 S235JR", 200, 100, 14, 15, 7.5))




for data in Table:
    print data[0]
    doc=FreeCAD.newDocument("Bar")
    sk1=doc.addObject('Sketcher::SketchObject','Sketch')
    sk1.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation  (0.000000,0.000000,0.000000,1.000000))

    sk1.addGeometry(Part.Line(App.Vector(0.000000,0.000000,0),App.Vector(45.000000,-0.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1)) 
    sk1.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',0)) 
    sk1.addGeometry(Part.Line(App.Vector(45.000000,0.000000,0),App.Vector(45.000000,10.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',1,1,0,2)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',1)) 
    sk1.addGeometry(Part.Line(App.Vector(45.000000,10.000000,0),App.Vector(10.000000,10.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',2)) 
    sk1.addGeometry(Part.Line(App.Vector(0.000000,0.000000,0),App.Vector(-0.000000,60.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',3,1,-1,1)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',3)) 
    sk1.addGeometry(Part.Line(App.Vector(0.000000,60.000000,0),App.Vector(10.000000,60.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',4,1,3,2)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',4)) 
    sk1.addGeometry(Part.Line(App.Vector(10.000000,60.000000,0),App.Vector(10.000000,10.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',5,1,4,2)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',5,2,2,2)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',5)) 
    sk1.fillet(5,2,App.Vector(10.000000,12.944019,0),App.Vector(13.634069,10.000000,0),2.944019)
    sk1.fillet(4,5,App.Vector(5.000000,60.000000,0),App.Vector(10.000000,53.121605,0),5.000000)
    sk1.fillet(2,1,App.Vector(41.697803,10.000000,0),App.Vector(45.000000,7.694688,0),2.511621)
    sk1.addConstraint(Sketcher.Constraint('DistanceX',0,45.000000)) 
    sk1.setDatum(17,App.Units.Quantity('45.000000 mm'))
    sk1.addConstraint(Sketcher.Constraint('DistanceY',3,60.000000)) 
    sk1.setDatum(18,App.Units.Quantity('60.000000 mm'))
    sk1.addConstraint(Sketcher.Constraint('DistanceY',0,2,2,1,10.000000)) 
    sk1.setDatum(19,App.Units.Quantity('10.000000 mm'))
    sk1.addConstraint(Sketcher.Constraint('DistanceX',3,2,5,1,10.000000)) 
    sk1.setDatum(20,App.Units.Quantity('10.000000 mm'))
    sk1.addConstraint(Sketcher.Constraint('Radius',6,2.944019)) 
    sk1.setDatum(21,App.Units.Quantity('1 mm'))
    sk1.addConstraint(Sketcher.Constraint('Radius',8,2.511621)) 
    sk1.setDatum(22,App.Units.Quantity('1 mm'))
    sk1.addConstraint(Sketcher.Constraint('Radius',7,5.000000)) 
    sk1.setDatum(23,App.Units.Quantity('1 mm'))
    sk1.delConstraint(1)
    sk1.setDatum(16,App.Units.Quantity(str(data[1])+' mm'))
    sk1.setDatum(17,App.Units.Quantity(str(data[2])+' mm'))
    sk1.setDatum(18,App.Units.Quantity(str(data[3])+' mm'))
    sk1.setDatum(19,App.Units.Quantity(str(data[3])+' mm'))
    sk1.setDatum(20,App.Units.Quantity(str(data[4])+' mm'))
    sk1.setDatum(21,App.Units.Quantity(str(data[5])+' mm'))
    sk1.setDatum(22,App.Units.Quantity(str(data[5])+' mm'))

    myEx=App.ActiveDocument.addObject("Part::Extrusion","Extrude")
    myEx.Base = sk1
    myEx.Dir = (0,0,50)
    myEx.Solid = (True)
    myEx.TaperAngle = (0)
    myEx.Label = data[0]

    Gui.getDocument(App.ActiveDocument.Name).getObject("Sketch").Visibility=False
    App.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.saveAs(LIBRARYPATH+'/Mechanical Parts/Profiles/EN10056 Unequal Angle Bars/'+data[0]+'.FCStd')
    __objs__=[]
    __objs__.append(FreeCAD.getDocument(App.ActiveDocument.Name).getObject("Extrude"))
    ImportGui.export(__objs__,LIBRARYPATH+'/Mechanical Parts/Profiles/EN10056 Unequal Angle Bars/'+data[0]+'.step')
    Mesh.export(__objs__,LIBRARYPATH+'/Mechanical Parts/Profiles/EN10056 Unequal Angle Bars/'+data[0]+'.stl')
    del __objs__
    App.closeDocument(App.ActiveDocument.Name)

print 'End'

 

 
 

