# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find.ui'
#
# Created: Thu Jun 21 20:50:53 2012
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
        self.lineEdit = QtGui.QLineEdit(Find)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.label = QtGui.QLabel(Find)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.hitlist = QtGui.QTreeWidget(Find)
        self.hitlist.setObjectName("hitlist")
        self.gridLayout.addWidget(self.hitlist, 4, 0, 1, 1)
        self.find = QtGui.QPushButton(Find)
        self.find.setObjectName("find")
        self.gridLayout.addWidget(self.find, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Find)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.retranslateUi(Find)
        QtCore.QMetaObject.connectSlotsByName(Find)

    def retranslateUi(self, Find):
        Find.setWindowTitle(QtGui.QApplication.translate("Find", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Find", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.hitlist.headerItem().setText(0, QtGui.QApplication.translate("Find", "Object", None, QtGui.QApplication.UnicodeUTF8))
        self.find.setText(QtGui.QApplication.translate("Find", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Find", "Click on results below to navigate to the result", None, QtGui.QApplication.UnicodeUTF8))

