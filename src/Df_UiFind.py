# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find.ui'
#
# Created: Thu Jun 21 21:26:10 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Find(object):
    def setupUi(self, Find):
        Find.setObjectName("Find")
        Find.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Find)
        self.gridLayout.setObjectName("gridLayout")
        self.input = QtGui.QLineEdit(Find)
        self.input.setObjectName("input")
        self.gridLayout.addWidget(self.input, 1, 0, 1, 1)
        self.heading = QtGui.QLabel(Find)
        self.heading.setObjectName("heading")
        self.gridLayout.addWidget(self.heading, 0, 0, 1, 1)
        self.instruction = QtGui.QLabel(Find)
        self.instruction.setObjectName("instruction")
        self.gridLayout.addWidget(self.instruction, 2, 0, 1, 1)
        self.hitlist = QtGui.QTreeWidget(Find)
        self.hitlist.setObjectName("hitlist")
        self.gridLayout.addWidget(self.hitlist, 3, 0, 1, 1)

        self.retranslateUi(Find)
        QtCore.QMetaObject.connectSlotsByName(Find)

    def retranslateUi(self, Find):
        Find.setWindowTitle(QtGui.QApplication.translate("Find", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.heading.setText(QtGui.QApplication.translate("Find", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.instruction.setText(QtGui.QApplication.translate("Find", "Click on results below to navigate to the result", None, QtGui.QApplication.UnicodeUTF8))
        self.hitlist.headerItem().setText(0, QtGui.QApplication.translate("Find", "Object", None, QtGui.QApplication.UnicodeUTF8))

