from PyQt6.QtCore import *
from PyQt6 import QtGui, QtWidgets
import Df, os, platform, subprocess, sys
from utils import *
import Df_Dialog


class GlobalButtons(object):
    def __init__(self, mw, configW, helpW):
        mw.configure.clicked.connect(self.configure)
        mw.help.clicked.connect(self.help)
        self.configW = configW
        
    def configure(self):
        self.configW.show()
        
    def help(self):
        Df_Dialog.TextDialog("Help", None, "helptext.html")
        
