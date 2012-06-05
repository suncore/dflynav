import sys
from PySide import QtCore, QtGui

from Df_UiMainwin import Ui_MainWindow
from Df_UiDialog import Ui_Dialog
from Df_UiConfig import Ui_Config
from Df_UiPreview import Ui_Preview
from Df_UiJobstatus import Ui_Jobstatus
from Df_UiHelp import Ui_Help
import os
import vfs


class Gui():
    pass

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

class Dialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

class Config(QtGui.QDialog, Ui_Config):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

class Help(QtGui.QDialog, Ui_Help):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

class Jobstatus(QtGui.QDialog, Ui_Jobstatus):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

class Preview(QtGui.QDialog, Ui_Preview):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
