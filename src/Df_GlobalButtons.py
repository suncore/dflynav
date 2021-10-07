from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
import Df, os, platform, subprocess, sys
from utils import *
import Df_Dialog


class GlobalButtons(object):
    def __init__(self, mw, configW, helpW):
        mw.refresh.clicked.connect(self.refresh)
        mw.configure.clicked.connect(self.configure)
        mw.help.clicked.connect(self.help)
        self.configW = configW
        
    def refresh(self):
        Df.d.lp.setPath(Df.d.lp.cd)
        Df.d.rp.setPath(Df.d.rp.cd)

    def configure(self):
        self.configW.show()
        
    def help(self):
        Df_Dialog.TextDialog("Help", None, "res/helptext.html")
        
