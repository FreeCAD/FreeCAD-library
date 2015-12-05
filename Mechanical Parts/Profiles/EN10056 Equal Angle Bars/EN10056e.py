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
 	 ("Angle Bar L20x20x3 EN10056 S235JR", 20, 20, 3, 3.5, 2),
 	 ("Angle Bar L25x25x3 EN10056 S235JR", 25, 25, 3, 3.5, 2),
 	 ("Angle Bar L25x25x4 EN10056 S235JR", 25, 25, 4, 3.5, 2),
 	 ("Angle Bar L30x30x3 EN10056 S235JR", 30, 30, 3, 5, 2.5),
 	 ("Angle Bar L30x30x4 EN10056 S235JR", 30, 30, 4, 5, 2.5),
 	 ("Angle Bar L30x30x5 EN10056 S235JR", 30, 30, 5, 5, 2.5),
 	 ("Angle Bar L35x35x3 EN10056 S235JR", 35, 35, 3, 5, 2.5),
 	 ("Angle Bar L35x35x4 EN10056 S235JR", 35, 35, 4, 5, 2.5),
 	 ("Angle Bar L35x35x5 EN10056 S235JR", 35, 35, 5, 5, 2.5),
 	 ("Angle Bar L40x40x3 EN10056 S235JR", 40, 40, 3, 6, 2),
 	 ("Angle Bar L40x40x4 EN10056 S235JR", 40, 40, 4, 6, 3),
 	 ("Angle Bar L40x40x5 EN10056 S235JR", 40, 40, 5, 6, 3),
 	 ("Angle Bar L45x45x3 EN10056 S235JR", 45, 45, 3, 7, 2),
 	 ("Angle Bar L45x45x4 EN10056 S235JR", 45, 45, 4, 7, 3.5),
 	 ("Angle Bar L45x45x5 EN10056 S235JR", 45, 45, 5, 7, 3.5),
 	 ("Angle Bar L50x50x4 EN10056 S235JR", 50, 50, 4, 7, 3.5),
 	 ("Angle Bar L50x50x5 EN10056 S235JR", 50, 50, 5, 7, 3.5),
 	 ("Angle Bar L50x50x6 EN10056 S235JR", 50, 50, 6, 7, 3.5),
 	 ("Angle Bar L50x50x7 EN10056 S235JR", 50, 50, 7, 7, 3.5),
 	 ("Angle Bar L55x55x5 EN10056 S235JR", 55, 55, 5, 8, 4),
 	 ("Angle Bar L55x55x6 EN10056 S235JR", 55, 55, 6, 8, 4),
 	 ("Angle Bar L60x60x5 EN10056 S235JR", 60, 60, 5, 8, 4),
 	 ("Angle Bar L60x60x6 EN10056 S235JR", 60, 60, 6, 8, 4),
 	 ("Angle Bar L60x60x8 EN10056 S235JR", 60, 60, 8, 8, 4),
 	 ("Angle Bar L65x65x6 EN10056 S235JR", 65, 65, 6, 9, 4.5),
 	 ("Angle Bar L65x65x7 EN10056 S235JR", 65, 65, 7, 9, 4.5),
 	 ("Angle Bar L65x65x8 EN10056 S235JR", 65, 65, 8, 9, 4.5),
 	 ("Angle Bar L70x70x6 EN10056 S235JR", 70, 70, 6, 10, 5),
 	 ("Angle Bar L70x70x7 EN10056 S235JR", 70, 70, 7, 10, 5),
 	 ("Angle Bar L70x70x8 EN10056 S235JR", 70, 70, 8, 10, 5),
 	 ("Angle Bar L70x70x9 EN10056 S235JR", 70, 70, 9, 10, 5),
 	 ("Angle Bar L75x75x7 EN10056 S235JR", 75, 75, 7, 10, 5),
 	 ("Angle Bar L75x75x8 EN10056 S235JR", 75, 75, 8, 10, 5),
 	 ("Angle Bar L80x80x6 EN10056 S235JR", 80, 80, 6, 10, 5),
 	 ("Angle Bar L80x80x8 EN10056 S235JR", 80, 80, 8, 10, 5),
 	 ("Angle Bar L80x80x10 EN10056 S235JR", 80, 80, 10, 10, 5),
 	 ("Angle Bar L90x90x6 EN10056 S235JR", 90, 90, 6, 10, 5),
 	 ("Angle Bar L90x90x7 EN10056 S235JR", 90, 90, 7, 10, 5),
 	 ("Angle Bar L90x90x8 EN10056 S235JR", 90, 90, 8, 10, 5),
 	 ("Angle Bar L90x90x9 EN10056 S235JR", 90, 90, 9, 10, 5),
 	 ("Angle Bar L90x90x10 EN10056 S235JR", 90, 90, 10, 10, 5),
 	 ("Angle Bar L100x100x6 EN10056 S235JR", 100, 100, 6, 12, 5), 
 	 ("Angle Bar L100x100x8 EN10056 S235JR", 100, 100, 8, 12, 6),
 	 ("Angle Bar L100x100x10 EN10056 S235JR", 100, 100, 10, 12, 6),
 	 ("Angle Bar L100x100x12 EN10056 S235JR", 100, 100, 12, 12, 6),
 	 ("Angle Bar L110x110x8 EN10056 S235JR", 110, 110, 8, 12, 6),
 	 ("Angle Bar L110x110x10 EN10056 S235JR", 110, 110, 10, 12, 6),
 	 ("Angle Bar L120x120x8 EN10056 S235JR", 120, 120, 8, 13, 6.5),
 	 ("Angle Bar L120x120x10 EN10056 S235JR", 120, 120, 10, 13, 6.5),
 	 ("Angle Bar L120x120x11 EN10056 S235JR", 120, 120, 11, 13, 6.5),
 	 ("Angle Bar L120x120x12 EN10056 S235JR", 120, 120, 12, 13, 6.5),
 	 ("Angle Bar L130x130x12 EN10056 S235JR", 130, 130, 12, 14, 7),
 	 ("Angle Bar L130x130x14 EN10056 S235JR", 130, 130, 14, 14, 7),
 	 ("Angle Bar L140x140x10 EN10056 S235JR", 140, 140, 10, 15, 7.5),
 	 ("Angle Bar L140x140x12 EN10056 S235JR", 140, 140, 12, 15, 7.5),
 	 ("Angle Bar L140x140x14 EN10056 S235JR", 140, 140, 14, 15, 7.5),
 	 ("Angle Bar L150x150x12 EN10056 S235JR", 150, 150, 12, 16, 8),
 	 ("Angle Bar L150x150x14 EN10056 S235JR", 150, 150, 14, 16, 8),
 	 ("Angle Bar L150x150x15 EN10056 S235JR", 150, 150, 15, 16, 8),
 	 ("Angle Bar L160x160x10 EN10056 S235JR", 160, 160, 10, 17, 8.5),
 	 ("Angle Bar L160x160x12 EN10056 S235JR", 160, 160, 12, 17, 8.5),
 	 ("Angle Bar L160x160x14 EN10056 S235JR", 160, 160, 14, 17, 8.5),
 	 ("Angle Bar L160x160x15 EN10056 S235JR", 160, 160, 15, 17, 8.5),
 	 ("Angle Bar L160x160x16 EN10056 S235JR", 160, 160, 16, 17, 8.5),
 	 ("Angle Bar L160x160x17 EN10056 S235JR", 160, 160, 17, 17, 8.5),
 	 ("Angle Bar L180x180x12 EN10056 S235JR", 180, 180, 12, 18, 9),
 	 ("Angle Bar L180x180x14 EN10056 S235JR", 180, 180, 14, 18, 9),
 	 ("Angle Bar L180x180x16 EN10056 S235JR", 180, 180, 16, 18, 9),
 	 ("Angle Bar L180x180x18 EN10056 S235JR", 180, 180, 18, 18, 9),
 	 ("Angle Bar L200x200x14 EN10056 S235JR", 200, 200, 14, 18, 9),
 	 ("Angle Bar L200x200x16 EN10056 S235JR", 200, 200, 16, 18, 9),
 	 ("Angle Bar L200x200x18 EN10056 S235JR", 200, 200, 18, 18, 9),
 	 ("Angle Bar L200x200x20 EN10056 S235JR", 200, 200, 20, 18, 9),
 	 ("Angle Bar L200x200x24 EN10056 S235JR", 200, 200, 24, 18, 9),
 	 ("Angle Bar L250x250x25 EN10056 S235JR", 250, 250, 25,  20, 10),
 	 ("Angle Bar L250x250x28 EN10056 S235JR", 250, 250, 28, 18, 9),
 	 ("Angle Bar L250x250x32 EN10056 S235JR", 250, 250, 32, 20, 10),
 	 ("Angle Bar L250x250x35 EN10056 S235JR", 250, 250, 35, 18, 9))



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
    App.ActiveDocument.saveAs(LIBRARYPATH+'/Mechanical Parts/Profiles/EN10056 Equal Angle Bars/'+data[0]+'.FCStd')
    __objs__=[]
    __objs__.append(FreeCAD.getDocument(App.ActiveDocument.Name).getObject("Extrude"))
    ImportGui.export(__objs__,LIBRARYPATH+'/Mechanical Parts/Profiles/EN10056 Equal Angle Bars/'+data[0]+'.step')
    Mesh.export(__objs__,LIBRARYPATH+'/Mechanical Parts/Profiles/EN10056 Equal Angle Bars/'+data[0]+'.stl')
    del __objs__
    App.closeDocument(App.ActiveDocument.Name)

print 'End'

 

 
 

