
# Actionbuttons are those buttons in the middle column that are dynamic, changing with selection

from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets

class ActionButton(QtWidgets.QPushButton):
    # self.df_
    pass

class ActionButtons():
    def __init__(self, layoutW, mainW):
        self.layoutW = layoutW
        self.mainW = mainW
        self.buttons = []

    def addButton(self, name, callback):
        button = ActionButton(self.mainW)
        self.layoutW.addWidget(button)
        button.setText(QtWidgets.QApplication.translate("MainWindow", name, None))
        if name == "Delete":
            #button.setStyleSheet('QPushButton {background-color: #700000; color: white;}')
            #button.setStyleSheet('QPushButton {color: #700000;}')
            button.setIcon(button.style().standardIcon(QtWidgets.QStyle.SP_DialogDiscardButton))
        button.clicked.connect(callback)
        self.buttons.append(button)

    def clearButtons(self):
        for w in self.buttons:
            w.deleteLater()
            self.layoutW.removeWidget(w)
        self.buttons = []
