# -*- coding: utf-8 -*-


from PySide import QtCore, QtGui
from SimNDT.gui.constants import *

class Ui_checkSimulationDialog(object):
    def setupUi(self, checkSimulationDialog):
        scaleUI = SCALE_UI
        checkSimulationDialog.setObjectName("checkSimulationDialog")
        checkSimulationDialog.resize(620*scaleUI, 220*scaleUI)
        checkSimulationDialog.setMinimumSize(QtCore.QSize(620*scaleUI, 220*scaleUI))
        checkSimulationDialog.setMaximumSize(QtCore.QSize(620*scaleUI, 220*scaleUI))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/check3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        checkSimulationDialog.setWindowIcon(icon)
        self.closePushButton = QtGui.QPushButton(checkSimulationDialog)
        self.closePushButton.setGeometry(QtCore.QRect(10*scaleUI, 180*scaleUI, 110*scaleUI, 32*scaleUI))
        self.closePushButton.setObjectName("closePushButton")
        self.treeWidget = QtGui.QTreeWidget(checkSimulationDialog)
        self.treeWidget.setGeometry(QtCore.QRect(10*scaleUI, 10*scaleUI, 601*scaleUI, 161*scaleUI))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")

        self.retranslateUi(checkSimulationDialog)
        QtCore.QMetaObject.connectSlotsByName(checkSimulationDialog)

    def retranslateUi(self, checkSimulationDialog):
        checkSimulationDialog.setWindowTitle(QtGui.QApplication.translate("checkSimulationDialog", "Check and Update Simulation Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.closePushButton.setText(QtGui.QApplication.translate("checkSimulationDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

