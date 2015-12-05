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

Table = (("Round Bar 6 EN10060 S235JR", 6),
         ("Round Bar 8 EN10060 S235JR", 8),
         ("Round Bar 9 EN10060 S235JR", 9),
         ("Round Bar 10 EN10060 S235JR", 10),
         ("Round Bar 12 EN10060 S235JR", 12),
         ("Round Bar 14 EN10060 S235JR", 14),
         ("Round Bar 15 EN10060 S235JR", 15),
         ("Round Bar 16 EN10060 S235JR", 16),
         ("Round Bar 18 EN10060 S235JR", 18),
         ("Round Bar 20 EN10060 S235JR", 20),
         ("Round Bar 22 EN10060 S235JR", 22),
         ("Round Bar 24 EN10060 S235JR", 24),
         ("Round Bar 25 EN10060 S235JR", 25),
         ("Round Bar 26 EN10060 S235JR", 26),
         ("Round Bar 28 EN10060 S235JR", 28),
         ("Round Bar 30 EN10060 S235JR", 30),
         ("Round Bar 32 EN10060 S235JR", 32),
         ("Round Bar 35 EN10060 S235JR", 35),
         ("Round Bar 40 EN10060 S235JR", 40),
         ("Round Bar 42 EN10060 S235JR", 42),
         ("Round Bar 45 EN10060 S235JR", 45),
         ("Round Bar 48 EN10060 S235JR", 48),
         ("Round Bar 50 EN10060 S235JR", 50),
         ("Round Bar 52 EN10060 S235JR", 52),
         ("Round Bar 55 EN10060 S235JR", 55),
         ("Round Bar 58 EN10060 S235JR", 58),
         ("Round Bar 60 EN10060 S235JR", 60),
         ("Round Bar 62 EN10060 S235JR", 62),
         ("Round Bar 65 EN10060 S235JR", 65),
         ("Round Bar 70 EN10060 S235JR", 70),
         ("Round Bar 72 EN10060 S235JR", 72),
         ("Round Bar 75 EN10060 S235JR", 75),
         ("Round Bar 80 EN10060 S235JR", 80),
         ("Round Bar 85 EN10060 S235JR", 85),
         ("Round Bar 90 EN10060 S235JR", 90),
         ("Round Bar 95 EN10060 S235JR", 95),
         ("Round Bar 100 EN10060 S235JR", 100),
         ("Round Bar 105 EN10060 S235JR", 105),
         ("Round Bar 110 EN10060 S235JR", 110),
         ("Round Bar 115 EN10060 S235JR", 115),
         ("Round Bar 120 EN10060 S235JR", 120),
         ("Round Bar 125 EN10060 S235JR", 125),
         ("Round Bar 130 EN10060 S235JR", 130),
         ("Round Bar 135 EN10060 S235JR", 135),
         ("Round Bar 140 EN10060 S235JR", 140),
         ("Round Bar 150 EN10060 S235JR", 150),
         ("Round Bar 160 EN10060 S235JR", 160),
         ("Round Bar 170 EN10060 S235JR", 170),
         ("Round Bar 180 EN10060 S235JR", 180),
         ("Round Bar 190 EN10060 S235JR", 190),
         ("Round Bar 200 EN10060 S235JR", 200),
         ("Round Bar 210 EN10060 S235JR", 210),
         ("Round Bar 220 EN10060 S235JR", 220),
         ("Round Bar 230 EN10060 S235JR", 230),
         ("Round Bar 240 EN10060 S235JR", 240),
         ("Round Bar 250 EN10060 S235JR", 250),
         ("Round Bar 260 EN10060 S235JR", 260),
         ("Round Bar 270 EN10060 S235JR", 270),
         ("Round Bar 280 EN10060 S235JR", 280),
         ("Round Bar 290 EN10060 S235JR", 290),
         ("Round Bar 300 EN10060 S235JR", 300),
         ("Round Bar 310 EN10060 S235JR", 310),
         ("Round Bar 330 EN10060 S235JR", 330),
         ("Round Bar 340 EN10060 S235JR", 340),
         ("Round Bar 360 EN10060 S235JR", 360),
         ("Round Bar 380 EN10060 S235JR", 380),
         ("Round Bar 400 EN10060 S235JR", 400))


for data in Table:
    print data[0]
    doc=FreeCAD.newDocument("Bar")
    sk1=doc.addObject('Sketcher::SketchObject','Sketch')
    sk1.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation  (0.000000,0.000000,0.000000,1.000000))

    sk1.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0),App.Vector(0,0,1),20.000000))
    sk1.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
    sk1.addConstraint(Sketcher.Constraint('Radius',0,20.000000)) 
    sk1.setDatum(1,App.Units.Quantity(str(data[1]/2)+' mm'))

    myEx=App.ActiveDocument.addObject("Part::Extrusion","Extrude")
    myEx.Base = sk1
    myEx.Dir = (0,0,50)
    myEx.Solid = (True)
    myEx.TaperAngle = (0)
    myEx.Label = data[0]

    Gui.getDocument(App.ActiveDocument.Name).getObject("Sketch").Visibility=False
    App.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")
    App.ActiveDocument.saveAs(LIBRARYPATH+'/Mechanical Parts/Profiles/EN10060 Round steel bars/'+data[0]+'.FCStd')
    __objs__=[]
    __objs__.append(FreeCAD.getDocument(App.ActiveDocument.Name).getObject("Extrude"))
    ImportGui.export(__objs__,LIBRARYPATH+'/Mechanical Parts/Profiles/EN10060 Round steel bars/'+data[0]+'.step')
    Mesh.export(__objs__,LIBRARYPATH+'/Mechanical Parts/Profiles/EN10060 Round steel bars/'+data[0]+'.stl')
    del __objs__
    App.closeDocument(App.ActiveDocument.Name)

print 'End'

 

 
 

