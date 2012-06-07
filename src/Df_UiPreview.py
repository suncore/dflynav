# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preview.ui'
#
# Created: Thu Jun  7 08:56:31 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Preview(object):
    def setupUi(self, Preview):
        Preview.setObjectName("Preview")
        Preview.resize(420, 420)
        self.gridLayout = QtGui.QGridLayout(Preview)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtGui.QGraphicsView(Preview)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.line = QtGui.QFrame(Preview)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.line1 = QtGui.QLabel(Preview)
        self.line1.setObjectName("line1")
        self.gridLayout.addWidget(self.line1, 2, 0, 1, 1)
        self.line2 = QtGui.QLabel(Preview)
        self.line2.setObjectName("line2")
        self.gridLayout.addWidget(self.line2, 3, 0, 1, 1)

        self.retranslateUi(Preview)
        QtCore.QMetaObject.connectSlotsByName(Preview)

    def retranslateUi(self, Preview):
        Preview.setWindowTitle(QtGui.QApplication.translate("Preview", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.line1.setText(QtGui.QApplication.translate("Preview", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.line2.setText(QtGui.QApplication.translate("Preview", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

