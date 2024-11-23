__author__ = 'Miguel Molero'



import os
from PySide.QtGui import *

from SimNDT.gui.ui_runsimulation import Ui_runSimulationDialog
from SimNDT.gui.Warnings import WarningParms
import SimNDT.gui.constants as c


class RunSimulation(QDialog, Ui_runSimulationDialog):

    def __init__(self, filename, Simulation, parent=None):

        super(RunSimulation, self).__init__(parent)
        self.setupUi(self)
        
        # Previous simulations etup, keep settings
        
        print(Simulation.lastSimulationSetup)

        self.lastSimulationSetup = Simulation.lastSimulationSetup

        self.filename = filename
        self.basename = None
        self.Simulation = Simulation

        self.receiverShow = False
        self.receiverCheckBox.setVisible(False)

        #self.ColormapView = ColorbarWidget()

        self.colormapComboBox.addItems(["jet","gray"])
        self.colormapComboBox.setCurrentIndex(0)
        self.colormapComboBox.setVisible(False)

        self.fieldSelectorComboBox.addItems(["Vx","Vy","[Vx,Vy]","Txx","Txy","Tyy","[Txx:Tyy]","Dx","Dy","[Dx,Dy]","SV"])
        self.fieldSelectorComboBox.setCurrentIndex(0)
        self.fieldSelectorComboBox.setVisible(False)


        self.stepsLabel.setVisible(False)

        self.snapshotStepLabel.setVisible(False)
        self.snapshotStepSpinBox.setVisible(False)


        self.visualizacionRangeLabel.setVisible(False)
        self.visualizacionRangeSpinBox.setVisible(False)

        self.enableSavingFieldsLabel.setVisible(False)
        self.enableSavingFieldsCheckBox.setVisible(False)
        self.enableSavingSignalsLabel.setVisible(False)
        self.enableSavingSignalsCheckBox.setVisible(False)
        self.enableSavingNumpyLabel.setVisible(False)
        self.enableSavingNumpyCheckBox.setVisible(False)
        self.enableSavingVolumeLabel.setVisible(False)
        self.enableSavingVolumeCheckBox.setVisible(False)
        self.enableSavingImagesLabel.setVisible(False)
        self.enableSavingImagesCheckBox.setVisible(False)
        self.fieldSelectorLabel.setVisible(False)
        self.fieldSelectorComboBox.setVisible(False)
        self.signalShapeLabel.setVisible(False)
        self.signalPlacementLabel.setVisible(False)
        self.signalSizeLabel.setVisible(False)
        self.signalShapeLineEdit.setVisible(False)
        self.signalPlacementLineEdit.setVisible(False)
        self.signalSizeLineEdit.setVisible(False)
        self.colormapComboBox.setVisible(True)

        #self.colormapLayout.addWidget(self.ColormapView)



        self.setLayout(self.verticalLayout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)


        self.viewCheckBox.stateChanged.connect(self.visualizacionRangeSpinBox.setVisible)
        self.viewCheckBox.stateChanged.connect(self.visualizacionRangeLabel.setVisible)
        self.viewCheckBox.stateChanged.connect(self.receiverCheckBox.setVisible)
        self.viewCheckBox.stateChanged.connect(self.colormapComboBox.setVisible)

        self.viewCheckBox.stateChanged.connect(self.receiveFunction)
        self.viewCheckBox.stateChanged.connect(self.updateColor)
        #self.colormapComboBox.activated.connect(self.ColormapView.Show)
        self.snapshotsPushButton.pressed.connect(self.snapshots)
        self.setWindowTitle("Simulation Run Setup")

        if self.lastSimulationSetup != None:
          self.viewCheckBox.setChecked(self.lastSimulationSetup["isView"])
          self.receiverCheckBox.setChecked(self.lastSimulationSetup["isReceiverPlot"])
          self.receiverShow=self.lastSimulationSetup["isReceiverPlot"]
          if self.lastSimulationSetup["isView"]:
            self.visualizacionRangeSpinBox.setVisible(True)
            self.visualizacionRangeLabel.setVisible(True)
            self.receiverCheckBox.setVisible(True)
            self.colormapComboBox.setVisible(True)
          self.colormapComboBox.setCurrentIndex(self.lastSimulationSetup["color"])
          self.visualizacionRangeSpinBox.setValue(self.lastSimulationSetup["dB"])
          self.fieldSelectorComboBox.setCurrentIndex(self.lastSimulationSetup["field"])
          self.signalShapeLineEdit.setText(','.join(str(x) for x in self.lastSimulationSetup["sensorShape"]))
          self.signalPlacementLineEdit.setText(','.join(str(x) for x in self.lastSimulationSetup["sensorPlacement"]))
          self.signalSizeLineEdit.setText(str(self.lastSimulationSetup["sensorSize"]))

    def snapshots(self):
        lastPath=''
        if self.lastSimulationSetup != None:
          lastPath=self.lastSimulationSetup["lastPath"]
        fname = self.filename if self.filename is not None else "."
        fname, filters =  QFileDialog.getSaveFileName(None, "Set Base Name for Snapshots", lastPath+os.path.splitext(fname)[0])
        self.basename  = os.path.splitext(fname)[0]
        if self.lastSimulationSetup != None:
          self.lastSimulationSetup["lastPath"] = os.path.dirname(fname)
          
        if self.basename is not None:

            if len(self.basename)!=0:
                self.snapshotStepLabel.setVisible(True)
                self.snapshotStepSpinBox.setVisible(True)

                self.stepsLabel.setVisible(True)
                self.stepsLabel.setText("Simulation Time Steps: %d"%(self.Simulation.TimeSteps))

                self.visualizacionRangeSpinBox.setVisible(True)
                self.visualizacionRangeLabel.setVisible(True)

                self.enableSavingFieldsLabel.setVisible(True)
                self.enableSavingFieldsCheckBox.setVisible(True)
                self.enableSavingSignalsLabel.setVisible(True)
                self.enableSavingSignalsCheckBox.setVisible(True)
                self.enableSavingNumpyLabel.setVisible(True)
                self.enableSavingNumpyCheckBox.setVisible(True)
                self.enableSavingVolumeLabel.setVisible(True)
                self.enableSavingVolumeCheckBox.setVisible(True)
                self.enableSavingImagesLabel.setVisible(True)
                self.enableSavingImagesCheckBox.setVisible(True)
                self.fieldSelectorLabel.setVisible(True)
                self.fieldSelectorComboBox.setVisible(True)
                self.signalShapeLabel.setVisible(True)
                self.signalPlacementLabel.setVisible(True)
                self.signalSizeLabel.setVisible(True)
                self.signalShapeLineEdit.setVisible(True)
                self.signalPlacementLineEdit.setVisible(True)
                self.signalSizeLineEdit.setVisible(True)

                self.colormapComboBox.setVisible(True)
                self.updateColor()
                
                if self.lastSimulationSetup != None:
                  self.enableSavingFieldsCheckBox.setChecked(self.lastSimulationSetup["isEnableFields"])
                  self.enableSavingSignalsCheckBox.setChecked(self.lastSimulationSetup["isEnableSignals"])
                  self.enableSavingNumpyCheckBox.setChecked(self.lastSimulationSetup["isEnableNumPy"])
                  self.enableSavingVolumeCheckBox.setChecked(self.lastSimulationSetup["isEnableVolume"])
                  self.enableSavingImagesCheckBox.setChecked(self.lastSimulationSetup["isEnableImages"])
                  self.snapshotStepSpinBox.setValue(self.lastSimulationSetup["step"])
                  self.visualizacionRangeSpinBox.setValue(self.lastSimulationSetup["dB"])
                  self.fieldSelectorComboBox.setCurrentIndex(self.lastSimulationSetup["field"])
                  self.signalShapeLineEdit.setText(','.join(str(x) for x in self.lastSimulationSetup["sensorShape"]))
                  self.signalPlacementLineEdit.setText(','.join(str(x) for x in self.lastSimulationSetup["sensorPlacement"]))
                  self.signalSizeLineEdit.setText(str(self.lastSimulationSetup["sensorSize"]))
                  

            else:
                self.basename = None

        else:

            self.basename = None


    def updateColor(self):
        self.colormapComboBox.setCurrentIndex(0)
        if self.lastSimulationSetup != None:
          self.colormapComboBox.setCurrentIndex(self.lastSimulationSetup["color"])
        #self.ColormapView.Show(0)
        QApplication.processEvents()


    def receiveFunction(self, value):
        self.receiverShow = value


