# -*- coding: utf-8 -*-


from PySide import QtCore, QtGui
from SimNDT.gui.constants import *

class Ui_generateVideoDialog(object):
    def setupUi(self, generateVideoDialog):
        scaleUI = SCALE_UI
        generateVideoDialog.setObjectName("generateVideoDialog")
        generateVideoDialog.resize(474*scaleUI, 261*scaleUI)
        generateVideoDialog.setMinimumSize(QtCore.QSize(474*scaleUI, 261*scaleUI))
        generateVideoDialog.setMaximumSize(QtCore.QSize(500*scaleUI, 300*scaleUI))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/snapshots.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        generateVideoDialog.setWindowIcon(icon)
        self.widget = QtGui.QWidget(generateVideoDialog)
        self.widget.setGeometry(QtCore.QRect(10*scaleUI, 10*scaleUI, 461*scaleUI, 241*scaleUI))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addImagesPushButton = QtGui.QPushButton(self.widget)
        self.addImagesPushButton.setObjectName("addImagesPushButton")
        self.verticalLayout.addWidget(self.addImagesPushButton)
        self.listWidget = QtGui.QListWidget(self.widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.videoBasenamePushButton = QtGui.QPushButton(self.widget)
        self.videoBasenamePushButton.setObjectName("videoBasenamePushButton")
        self.horizontalLayout.addWidget(self.videoBasenamePushButton)
        self.videoBasenameLineEdit = QtGui.QLineEdit(self.widget)
        self.videoBasenameLineEdit.setReadOnly(True)
        self.videoBasenameLineEdit.setObjectName("videoBasenameLineEdit")
        self.horizontalLayout.addWidget(self.videoBasenameLineEdit)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.fPSLabel = QtGui.QLabel(self.widget)
        self.fPSLabel.setObjectName("fPSLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.fPSLabel)
        self.fPSSpinBox = QtGui.QSpinBox(self.widget)
        self.fPSSpinBox.setMinimum(1)
        self.fPSSpinBox.setMaximum(30)
        self.fPSSpinBox.setObjectName("fPSSpinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.fPSSpinBox)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(generateVideoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), generateVideoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), generateVideoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(generateVideoDialog)

    def retranslateUi(self, generateVideoDialog):
        generateVideoDialog.setWindowTitle(QtGui.QApplication.translate("generateVideoDialog", "Generate Video ", None, QtGui.QApplication.UnicodeUTF8))
        generateVideoDialog.setToolTip(QtGui.QApplication.translate("generateVideoDialog", "Generate Video from Snapshots", None, QtGui.QApplication.UnicodeUTF8))
        self.addImagesPushButton.setText(QtGui.QApplication.translate("generateVideoDialog", "Add Images", None, QtGui.QApplication.UnicodeUTF8))
        self.videoBasenamePushButton.setText(QtGui.QApplication.translate("generateVideoDialog", "Set Video Name", None, QtGui.QApplication.UnicodeUTF8))
        self.fPSLabel.setText(QtGui.QApplication.translate("generateVideoDialog", "FPS", None, QtGui.QApplication.UnicodeUTF8))


