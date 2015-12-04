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

Table = (("Square Bar 8 EN10059 S235JR", 8),
         ("Square Bar 10 EN10059 S235JR", 10),
         ("Square Bar 12 EN10059 S235JR", 12),
         ("Square Bar 14 EN10059 S235JR", 14),
         ("Square Bar 15 EN10059 S235JR", 15),
         ("Square Bar 16 EN10059 S235JR", 16),
         ("Square Bar 18 EN10059 S235JR", 18),
         ("Square Bar 20 EN10059 S235JR", 20),
         ("Square Bar 25 EN10059 S235JR", 25),
         ("Square Bar 30 EN10059 S235JR", 30),
         ("Square Bar 35 EN10059 S235JR", 35),
         ("Square Bar 40 EN10059 S235JR", 40),
         ("Square Bar 45 EN10059 S235JR", 45),
         ("Square Bar 50 EN10059 S235JR", 50),
         ("Square Bar 55 EN10059 S235JR", 55),
         ("Square Bar 60 EN10059 S235JR", 60),
         ("Square Bar 65 EN10059 S235JR", 65),
         ("Square Bar 70 EN10059 S235JR", 70),
         ("Square Bar 75 EN10059 S235JR", 75),
         ("Square Bar 80 EN10059 S235JR", 80),
         ("Square Bar 90 EN10059 S235JR", 90),
         ("Square Bar 100 EN10059 S235JR", 100),
         ("Square Bar 110 EN10059 S235JR", 110),
         ("Square Bar 120 EN10059 S235JR", 120),
         ("Square Bar 125 EN10059 S235JR", 125),
         ("Square Bar 130 EN10059 S235JR", 130),
         ("Square Bar 135 EN10059 S235JR", 135),
         ("Square Bar 140 EN10059 S235JR", 140),
         ("Square Bar 150 EN10059 S235JR", 150),
         ("Square Bar 160 EN10059 S235JR", 160),
         ("Square Bar 170 EN10059 S235JR", 170),
         ("Square Bar 180 EN10059 S235JR", 180),
         ("Square Bar 200 EN10059 S235JR", 200),
         ("Square Bar 220 EN10059 S235JR", 220),
         ("Square Bar 240 EN10059 S235JR", 240))


for data in Table:
    print data[0]
    doc=FreeCAD.newDocument("Bar")
    sk1=doc.addObject('Sketcher::SketchObject','Sketch')
    sk1.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation  (0.000000,0.000000,0.000000,1.000000))

    sk1.addGeometry(Part.Line(App.Vector(-10.000000,-10.000000,0),App.Vector(10.000000,-10.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(10.000000,-10.000000,0),App.Vector(10.000000,10.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(10.000000,10.000000,0),App.Vector(-10.000000,10.000000,0)))
    sk1.addGeometry(Part.Line(App.Vector(-10.000000,10.000000,0),App.Vector(-10.000000,-10.000000,0)))
    sk1.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
    sk1.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',0)) 
    sk1.addConstraint(Sketcher.Constraint('Horizontal',2)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',1)) 
    sk1.addConstraint(Sketcher.Constraint('Vertical',3)) 
    sk1.addConstraint(Sketcher.Constraint('Symmetric',1,2,0,2,-1)) 
    sk1.addConstraint(Sketcher.Constraint('Symmetric',2,2,1,2,-2)) 
    sk1.addConstraint(Sketcher.Constraint('Equal',1,2)) 
    sk1.addConstraint(Sketcher.Constraint('DistanceY',1,20.000000)) 
    sk1.setDatum(11,App.Units.Quantity(str(data[1])+' mm'))

    myEx=App.ActiveDocument.addObject("Part::Extrusion","Extrude")
    myEx.Base = sk1
    myEx.Dir = (0,0,50)
    myEx.Solid = (True)
    myEx.TaperAngle = (0)
    myEx.Label = 'Extrude'

    Gui.getDocument(App.ActiveDocument.Name).getObject("Sketch").Visibility=False
    App.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.saveAs(LIBRARYPATH+'/Mechanical Parts/Profiles/EN10059 Recangular steel bars/'+data[0]+'.FCStd')
    __objs__=[]
    __objs__.append(FreeCAD.getDocument(App.ActiveDocument.Name).getObject("Extrude"))
    ImportGui.export(__objs__,LIBRARYPATH+'/Mechanical Parts/Profiles/EN10059 Recangular steel bars/'+data[0]+'.step')
    Mesh.export(__objs__,LIBRARYPATH+'/Mechanical Parts/Profiles/EN10059 Recangular steel bars/'+data[0]+'.stl')
    del __objs__
    App.closeDocument(App.ActiveDocument.Name)

print 'End'

 

 
 

