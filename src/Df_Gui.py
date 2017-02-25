import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets

from Df_UiMainwin import Ui_MainWindow
#from Df_UiDialog import Ui_Dialog
from Df_UiConfig import Ui_Config
#from Df_UiPreview import Ui_Preview
from Df_UiJobstatus import Ui_Jobstatus
from Df_UiHelp import Ui_Help
from Df_UiFind import Ui_Find
import os
import vfs


class Gui():
    pass

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

#class Dialog(QtWidgets.QDialog, Ui_Dialog):
#    def __init__(self, parent=None):
#        QtWidgets.QDialog.__init__(self, parent)
#        self.setupUi(self)

class Config(QtWidgets.QDialog, Ui_Config):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

class Help(QtWidgets.QDialog, Ui_Help):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

class Find(QtWidgets.QDialog, Ui_Find):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

class Jobstatus(QtWidgets.QDialog, Ui_Jobstatus):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

#class Preview(QtWidgets.QDialog, Ui_Preview):
#    def __init__(self, parent=None):
#        QtWidgets.QDialog.__init__(self, parent)
#        self.setupUi(self)
