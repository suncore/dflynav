# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created: Thu May  3 13:33:31 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Config(object):
    def setupUi(self, Config):
        Config.setObjectName("Config")
        Config.resize(563, 276)
        self.gridLayout = QtGui.QGridLayout(Config)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(Config)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Config)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.showHidden = QtGui.QCheckBox(self.groupBox_2)
        self.showHidden.setTristate(False)
        self.showHidden.setObjectName("showHidden")
        self.gridLayout_3.addWidget(self.showHidden, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(Config)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rememberStartFolders = QtGui.QRadioButton(self.groupBox)
        self.rememberStartFolders.setChecked(True)
        self.rememberStartFolders.setObjectName("rememberStartFolders")
        self.gridLayout_2.addWidget(self.rememberStartFolders, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.leftStartDir = QtGui.QLineEdit(self.groupBox)
        self.leftStartDir.setObjectName("leftStartDir")
        self.gridLayout_2.addWidget(self.leftStartDir, 4, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 1)
        self.rightStartDir = QtGui.QLineEdit(self.groupBox)
        self.rightStartDir.setObjectName("rightStartDir")
        self.gridLayout_2.addWidget(self.rightStartDir, 6, 0, 1, 1)
        self.startAtSpecifiedFolders = QtGui.QRadioButton(self.groupBox)
        self.startAtSpecifiedFolders.setObjectName("startAtSpecifiedFolders")
        self.gridLayout_2.addWidget(self.startAtSpecifiedFolders, 1, 0, 1, 1)
        self.useCurrentLeft = QtGui.QPushButton(self.groupBox)
        self.useCurrentLeft.setObjectName("useCurrentLeft")
        self.gridLayout_2.addWidget(self.useCurrentLeft, 4, 1, 1, 1)
        self.useCurrentRight = QtGui.QPushButton(self.groupBox)
        self.useCurrentRight.setObjectName("useCurrentRight")
        self.gridLayout_2.addWidget(self.useCurrentRight, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Config)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Config.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Config.reject)
        QtCore.QMetaObject.connectSlotsByName(Config)

    def retranslateUi(self, Config):
        Config.setWindowTitle(QtGui.QApplication.translate("Config", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Config", "Miscellaneous", None, QtGui.QApplication.UnicodeUTF8))
        self.showHidden.setText(QtGui.QApplication.translate("Config", "Show hidden files", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Config", "Start directories", None, QtGui.QApplication.UnicodeUTF8))
        self.rememberStartFolders.setText(QtGui.QApplication.translate("Config", "Remember start directories from last run", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Config", "Left start folder", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Config", "Right start folder", None, QtGui.QApplication.UnicodeUTF8))
        self.startAtSpecifiedFolders.setText(QtGui.QApplication.translate("Config", "Always start at specified directories", None, QtGui.QApplication.UnicodeUTF8))
        self.useCurrentLeft.setText(QtGui.QApplication.translate("Config", "Use current", None, QtGui.QApplication.UnicodeUTF8))
        self.useCurrentRight.setText(QtGui.QApplication.translate("Config", "Use current", None, QtGui.QApplication.UnicodeUTF8))
