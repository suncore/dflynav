import sys
from PySide import QtCore, QtGui

from Df_UiMainwin import Ui_MainWindow
import os
import vfs


class Gui():
    pass

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
