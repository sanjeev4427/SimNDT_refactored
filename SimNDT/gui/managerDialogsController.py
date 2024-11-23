__author__ = 'Miguel Molero'



import os
import copy
import subprocess

from PySide.QtCore import *
from PySide.QtGui import *



from SimNDT.gui.materialSetupController import MaterialSetup
from SimNDT.gui.boundarySetupController import BoundarySetup
from SimNDT.gui.singleLaunchSetupController import SingleLaunchSetup
from SimNDT.gui.linearScanController import LinearScanSetup
from SimNDT.gui.tomographySetupController import TomographySetup

# from SimNDT.gui.simulationSetupController import SimulationSetup
# from SimNDT.gui.checkSimulationController import CheckSimulation
from SimNDT.gui.runSimulationController import RunSimulation
from SimNDT.gui.engineController import EngineController
from SimNDT.gui.generateVideoController import GenerateVideo

from SimNDT.gui.twoPhaseModelDryCaseController import TwoPhaseModelDryCaseDialog
from SimNDT.gui.threePhaseModelDryCaseController import ThreePhaseModelDryCaseDialog
from SimNDT.gui.twoPhaseModelImmersionCaseController import TwoPhaseModelImmersionCaseDialog
from SimNDT.gui.threePhaseModelImmersionCaseController import ThreePhaseModelImmersionCaseDialog

from SimNDT.core.scenario import Scenario
from SimNDT.core.geometryObjects import Ellipse, Circle, Square, Rectangle
from SimNDT.core.simPack import SimPack
from SimNDT.core.receivers import Receivers

from SimNDT.gui.snapshots import SnapShots
from SimNDT.gui.Warnings import WarningParms, DoneParms
from SimNDT.gui import HelperMethods


from SimNDT.core.concreteModel import TwoPhaseModel


import numpy as np

def toIntList(stringList):
  splitList = stringList.split(',')
  if len(splitList)==1:
    if splitList[0]=='':
      splitList=[] # empty list
  return [int(x) for x in splitList]    



def singleLaunchSetup(self):

    dlg = SingleLaunchSetup(self.SimNDT_Scenario, self.SimNDT_Source, self.SimNDT_Inspection, self.SimNDT_Transducers, self.SimNDT_Signal)
    if dlg.exec_():

        self.SimNDT_Source = copy.deepcopy(dlg.Source)
        self.SimNDT_Transducers = copy.deepcopy(dlg.Transducers)
        self.SimNDT_Inspection = copy.deepcopy(dlg.Inspection)
        self.SimNDT_Signal = copy.deepcopy(dlg.Signal)

        self.SimNDT_Check = False
        self.dirty = True
        self.updateUI()





# def checkSimulation(self):

#     dlg = CheckSimulation(self.SimNDT_Scenario, self.SimNDT_Materials, self.SimNDT_Boundaries,
#                           self.SimNDT_Transducers, self.SimNDT_Inspection, self.SimNDT_Signal, self.SimNDT_Simulation)

#     self.SimNDT_Check = False

#     if dlg.exec_():
#         self.SimNDT_Check = True

#     self.SimNDT_Scenario = copy.deepcopy(dlg.Scenario)
#     self.SimNDT_Boundaries = copy.deepcopy(dlg.Boundaries)
#     self.SimNDT_Inspection = copy.deepcopy(dlg.Inspection)
#     self.dirty = True
#     self.OpenSimFile = False
#     self.updateUI()



def runEngine(SimNDT_Scenario, SimNDT_Materials, SimNDT_Boundaries,\
                    SimNDT_Inspection, SimNDT_Source, SimNDT_Transducers, \
                    SimNDT_Signal, SimNDT_Simulation):
    
    simPack = SimPack(SimNDT_Scenario, SimNDT_Materials, \
                        SimNDT_Boundaries, SimNDT_Inspection, SimNDT_Source, \
                        SimNDT_Transducers, SimNDT_Signal, SimNDT_Simulation)

    engine = EngineController(simPack)


    state = engine.run()

    if state == "Stop":
        print("Stop by User!!!!!")
    else:
        print("Simulation Done.")

    SimNDT_Receivers = Receivers(self.SimNDT_Inspection.Name)
    SimNDT_Receivers.setReceivers(engine)



