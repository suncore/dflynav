# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jobstatus.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Jobstatus(object):
    def setupUi(self, Jobstatus):
        Jobstatus.setObjectName("Jobstatus")
        Jobstatus.setWindowModality(QtCore.Qt.ApplicationModal)
        Jobstatus.resize(538, 425)
        self.gridLayout = QtWidgets.QGridLayout(Jobstatus)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stop = QtWidgets.QPushButton(Jobstatus)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)
        self.start = QtWidgets.QPushButton(Jobstatus)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        self.close = QtWidgets.QPushButton(Jobstatus)
        self.close.setObjectName("close")
        self.horizontalLayout.addWidget(self.close)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 3, 2)
        self.status = QtWidgets.QLabel(Jobstatus)
        self.status.setObjectName("status")
        self.gridLayout.addWidget(self.status, 2, 0, 1, 2)
        self.output = QtWidgets.QPlainTextEdit(Jobstatus)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 0, 0, 1, 2)

        self.retranslateUi(Jobstatus)
        QtCore.QMetaObject.connectSlotsByName(Jobstatus)

    def retranslateUi(self, Jobstatus):
        _translate = QtCore.QCoreApplication.translate
        Jobstatus.setWindowTitle(_translate("Jobstatus", "Job status"))
        self.stop.setText(_translate("Jobstatus", "Stop Job"))
        self.start.setText(_translate("Jobstatus", "Start Job"))
        self.close.setText(_translate("Jobstatus", "Close"))
        self.status.setText(_translate("Jobstatus", "status"))

