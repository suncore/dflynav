
from PySide.QtCore import *
from PySide import QtGui

class ActionButton(QtGui.QPushButton):
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
        button.setText(QtGui.QApplication.translate("MainWindow", name, None, QtGui.QApplication.UnicodeUTF8))
        button.clicked.connect(callback)
        self.buttons.append(button)

    def clearButtons(self):
        for w in self.buttons:
            w.deleteLater()
            self.layoutW.removeWidget(w)
        self.buttons = []
