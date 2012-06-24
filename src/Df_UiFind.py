# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find.ui'
#
# Created: Sun Jun 24 10:21:59 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Find(object):
    def setupUi(self, Find):
        Find.setObjectName("Find")
        Find.resize(569, 390)
        self.gridLayout = QtGui.QGridLayout(Find)
        self.gridLayout.setObjectName("gridLayout")
        self.heading = QtGui.QLabel(Find)
        self.heading.setObjectName("heading")
        self.gridLayout.addWidget(self.heading, 0, 0, 1, 1)
        self.input = QtGui.QLineEdit(Find)
        self.input.setObjectName("input")
        self.gridLayout.addWidget(self.input, 1, 0, 1, 1)
        self.recursive = QtGui.QCheckBox(Find)
        self.recursive.setObjectName("recursive")
        self.gridLayout.addWidget(self.recursive, 2, 0, 1, 1)
        self.hitlist = QtGui.QTreeWidget(Find)
        self.hitlist.setObjectName("hitlist")
        self.gridLayout.addWidget(self.hitlist, 8, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start = QtGui.QPushButton(Find)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        self.stop = QtGui.QPushButton(Find)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        self.instruction = QtGui.QLabel(Find)
        self.instruction.setObjectName("instruction")
        self.gridLayout.addWidget(self.instruction, 6, 0, 1, 1)
        self.status = QtGui.QLabel(Find)
        self.status.setObjectName("status")
        self.gridLayout.addWidget(self.status, 3, 0, 1, 1)
        self.close = QtGui.QPushButton(Find)
        self.close.setObjectName("close")
        self.gridLayout.addWidget(self.close, 9, 0, 1, 1)
        self.currentSearch = QtGui.QLabel(Find)
        self.currentSearch.setObjectName("currentSearch")
        self.gridLayout.addWidget(self.currentSearch, 4, 0, 1, 1)

        self.retranslateUi(Find)
        QtCore.QMetaObject.connectSlotsByName(Find)

    def retranslateUi(self, Find):
        Find.setWindowTitle(QtGui.QApplication.translate("Find", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.heading.setText(QtGui.QApplication.translate("Find", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.recursive.setText(QtGui.QApplication.translate("Find", "Search sub-folders recursively", None, QtGui.QApplication.UnicodeUTF8))
        self.hitlist.headerItem().setText(0, QtGui.QApplication.translate("Find", "Object", None, QtGui.QApplication.UnicodeUTF8))
        self.start.setText(QtGui.QApplication.translate("Find", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.stop.setText(QtGui.QApplication.translate("Find", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.instruction.setText(QtGui.QApplication.translate("Find", "Click on results below to navigate to the result", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setText(QtGui.QApplication.translate("Find", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("Find", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.currentSearch.setText(QtGui.QApplication.translate("Find", "Current searching for", None, QtGui.QApplication.UnicodeUTF8))

