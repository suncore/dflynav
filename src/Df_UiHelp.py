# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created: Mon Jun 11 20:10:19 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.setWindowModality(QtCore.Qt.ApplicationModal)
        Help.resize(513, 557)
        Help.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Help)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(Help)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.helpText = QtGui.QTextEdit(Help)
        self.helpText.setObjectName("helpText")
        self.gridLayout.addWidget(self.helpText, 0, 0, 1, 1)

        self.retranslateUi(Help)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Help.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Help.reject)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        Help.setWindowTitle(QtGui.QApplication.translate("Help", "Help", None, QtGui.QApplication.UnicodeUTF8))

