# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jobstatus.ui'
#
# Created: Sun Jun 24 10:21:59 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Jobstatus(object):
    def setupUi(self, Jobstatus):
        Jobstatus.setObjectName("Jobstatus")
        Jobstatus.setWindowModality(QtCore.Qt.ApplicationModal)
        Jobstatus.resize(538, 425)
        self.gridLayout = QtGui.QGridLayout(Jobstatus)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stop = QtGui.QPushButton(Jobstatus)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)
        self.start = QtGui.QPushButton(Jobstatus)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        self.close = QtGui.QPushButton(Jobstatus)
        self.close.setObjectName("close")
        self.horizontalLayout.addWidget(self.close)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 3, 2)
        self.status = QtGui.QLabel(Jobstatus)
        self.status.setObjectName("status")
        self.gridLayout.addWidget(self.status, 2, 0, 1, 2)
        self.output = QtGui.QPlainTextEdit(Jobstatus)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 0, 0, 1, 2)

        self.retranslateUi(Jobstatus)
        QtCore.QMetaObject.connectSlotsByName(Jobstatus)

    def retranslateUi(self, Jobstatus):
        Jobstatus.setWindowTitle(QtGui.QApplication.translate("Jobstatus", "Job status", None, QtGui.QApplication.UnicodeUTF8))
        self.stop.setText(QtGui.QApplication.translate("Jobstatus", "Stop Job", None, QtGui.QApplication.UnicodeUTF8))
        self.start.setText(QtGui.QApplication.translate("Jobstatus", "Start Job", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("Jobstatus", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setText(QtGui.QApplication.translate("Jobstatus", "status", None, QtGui.QApplication.UnicodeUTF8))

