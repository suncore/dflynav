# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Find(object):
    def setupUi(self, Find):
        Find.setObjectName("Find")
        Find.resize(569, 390)
        self.gridLayout = QtWidgets.QGridLayout(Find)
        self.gridLayout.setObjectName("gridLayout")
        self.heading = QtWidgets.QLabel(Find)
        self.heading.setObjectName("heading")
        self.gridLayout.addWidget(self.heading, 0, 0, 1, 1)
        self.input = QtWidgets.QLineEdit(Find)
        self.input.setObjectName("input")
        self.gridLayout.addWidget(self.input, 1, 0, 1, 1)
        self.recursive = QtWidgets.QCheckBox(Find)
        self.recursive.setObjectName("recursive")
        self.gridLayout.addWidget(self.recursive, 2, 0, 1, 1)
        self.hitlist = QtWidgets.QTreeWidget(Find)
        self.hitlist.setObjectName("hitlist")
        self.gridLayout.addWidget(self.hitlist, 8, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start = QtWidgets.QPushButton(Find)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        self.stop = QtWidgets.QPushButton(Find)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        self.instruction = QtWidgets.QLabel(Find)
        self.instruction.setObjectName("instruction")
        self.gridLayout.addWidget(self.instruction, 6, 0, 1, 1)
        self.status = QtWidgets.QLabel(Find)
        self.status.setObjectName("status")
        self.gridLayout.addWidget(self.status, 3, 0, 1, 1)
        self.close = QtWidgets.QPushButton(Find)
        self.close.setObjectName("close")
        self.gridLayout.addWidget(self.close, 9, 0, 1, 1)
        self.currentSearch = QtWidgets.QLabel(Find)
        self.currentSearch.setObjectName("currentSearch")
        self.gridLayout.addWidget(self.currentSearch, 4, 0, 1, 1)

        self.retranslateUi(Find)
        QtCore.QMetaObject.connectSlotsByName(Find)

    def retranslateUi(self, Find):
        _translate = QtCore.QCoreApplication.translate
        Find.setWindowTitle(_translate("Find", "Find"))
        self.heading.setText(_translate("Find", "TextLabel"))
        self.recursive.setText(_translate("Find", "Search sub-folders recursively"))
        self.hitlist.headerItem().setText(0, _translate("Find", "Object"))
        self.start.setText(_translate("Find", "Start"))
        self.stop.setText(_translate("Find", "Stop"))
        self.instruction.setText(_translate("Find", "Click on results below to navigate to the result"))
        self.status.setText(_translate("Find", "Status"))
        self.close.setText(_translate("Find", "Close"))
        self.currentSearch.setText(_translate("Find", "Current searching for"))

