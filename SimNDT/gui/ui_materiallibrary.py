# -*- coding: utf-8 -*-


from PySide import QtCore, QtGui
from SimNDT.gui.constants import *

class Ui_materialLibraryDialog(object):
    def setupUi(self, materialLibraryDialog):
        scaleUI = SCALE_UI
        materialLibraryDialog.setObjectName("materialLibraryDialog")
        materialLibraryDialog.resize(514*scaleUI, 371*scaleUI)
        materialLibraryDialog.setMinimumSize(QtCore.QSize(514*scaleUI, 371*scaleUI))
        materialLibraryDialog.setMaximumSize(QtCore.QSize(514*scaleUI, 371*scaleUI))
        self.materialListWidget = QtGui.QListWidget(materialLibraryDialog)
        self.materialListWidget.setGeometry(QtCore.QRect(20*scaleUI, 20*scaleUI, 221*scaleUI, 331*scaleUI))
        self.materialListWidget.setObjectName("materialListWidget")
        self.frame = QtGui.QFrame(materialLibraryDialog)
        self.frame.setGeometry(QtCore.QRect(250*scaleUI, 20*scaleUI, 241*scaleUI, 331*scaleUI))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.materialNameLineEdit = QtGui.QLineEdit(self.frame)
        self.materialNameLineEdit.setGeometry(QtCore.QRect(10*scaleUI, 10*scaleUI, 221*scaleUI, 21*scaleUI))
        self.materialNameLineEdit.setObjectName("materialNameLineEdit")
        self.infoLabel = QtGui.QLabel(self.frame)
        self.infoLabel.setGeometry(QtCore.QRect(20*scaleUI, 50*scaleUI, 201*scaleUI, 151*scaleUI))
        self.infoLabel.setAutoFillBackground(False)
        self.infoLabel.setObjectName("infoLabel")
        self.okPushButton = QtGui.QPushButton(self.frame)
        self.okPushButton.setGeometry(QtCore.QRect(10*scaleUI, 290*scaleUI, 110*scaleUI, 32*scaleUI))
        self.okPushButton.setObjectName("okPushButton")
        self.cancelPushButton = QtGui.QPushButton(self.frame)
        self.cancelPushButton.setGeometry(QtCore.QRect(120*scaleUI, 290*scaleUI, 110*scaleUI, 32*scaleUI))
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.createLibraryPushButton = QtGui.QPushButton(self.frame)
        self.createLibraryPushButton.setGeometry(QtCore.QRect(10*scaleUI, 220*scaleUI, 221*scaleUI, 32*scaleUI))
        self.createLibraryPushButton.setObjectName("createLibraryPushButton")
        self.createTemplatePushButton = QtGui.QPushButton(self.frame)
        self.createTemplatePushButton.setGeometry(QtCore.QRect(10*scaleUI, 250*scaleUI, 221*scaleUI, 32*scaleUI))
        self.createTemplatePushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.createTemplatePushButton.setObjectName("createTemplatePushButton")

        self.retranslateUi(materialLibraryDialog)
        QtCore.QMetaObject.connectSlotsByName(materialLibraryDialog)

    def retranslateUi(self, materialLibraryDialog):
        materialLibraryDialog.setWindowTitle(QtGui.QApplication.translate("materialLibraryDialog", "Material Library", None, QtGui.QApplication.UnicodeUTF8))
        self.materialNameLineEdit.setPlaceholderText(QtGui.QApplication.translate("materialLibraryDialog", "Selected Material", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("materialLibraryDialog", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.okPushButton.setText(QtGui.QApplication.translate("materialLibraryDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelPushButton.setText(QtGui.QApplication.translate("materialLibraryDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.createLibraryPushButton.setText(QtGui.QApplication.translate("materialLibraryDialog", "Load Custom Material Library", None, QtGui.QApplication.UnicodeUTF8))
        self.createTemplatePushButton.setText(QtGui.QApplication.translate("materialLibraryDialog", "Create Library Template", None, QtGui.QApplication.UnicodeUTF8))

