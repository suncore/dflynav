# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.setWindowModality(QtCore.Qt.ApplicationModal)
        Help.resize(581, 557)
        Help.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Help)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Help)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.helpText = QtWidgets.QTextEdit(Help)
        self.helpText.setObjectName("helpText")
        self.gridLayout.addWidget(self.helpText, 0, 0, 1, 1)

        self.retranslateUi(Help)
        self.buttonBox.accepted.connect(Help.accept)
        self.buttonBox.rejected.connect(Help.reject)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        _translate = QtCore.QCoreApplication.translate
        Help.setWindowTitle(_translate("Help", "Help"))

