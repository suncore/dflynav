from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
import Df, os, platform, subprocess, sys
from utils import *
import Df_Dialog


class GlobalButtons(object):
    def __init__(self, mw, configW, helpW):
        mw.refresh.clicked.connect(self.refresh)
        mw.configure.clicked.connect(self.configure)
        #mw.help.clicked.connect(self.help)
        self.configW = configW
        self.helpMenu = QtWidgets.QMenu(mw)
        mw.help.setMenu(self.helpMenu)
        actions = []
        action = QtWidgets.QAction("Help", mw)
        action.triggered.connect(self.help)
        actions.append(action)
        #action = QtWidgets.QAction("Show license key", mw)
        #action.triggered.connect(self.help_license)
        #actions.append(action)
        #action = QtWidgets.QAction("Enter license key", mw)
        #action.triggered.connect(Df.d.config.enterLicenseKey)
        #actions.append(action)
        #action = QtWidgets.QAction("License agreement", mw)
        #action.triggered.connect(self.help_agreement)
        #actions.append(action)
        action = QtWidgets.QAction("About", mw)
        action.triggered.connect(self.help_about)
        actions.append(action)
        self.helpMenu.addActions(actions)
        
    def refresh(self):
        Df.d.lp.setPath(Df.d.lp.cd)
        Df.d.rp.setPath(Df.d.rp.cd)

    def configure(self):
        self.configW.show()
        
    def help(self):
        Df_Dialog.TextDialog("Help", None, "res/helptext.html")

    def help_agreement(self):
        Df_Dialog.TextDialog("License", None, "res/license.html")

#    def help_license(self):
#        if Df.d.licenseKey == "":
#            Df_Dialog.MessageInfo("License", "No license key found.")
#        else:
#            Df_Dialog.MessageInfo("License", "License key (valid): " + Df.d.licenseKey)

    def help_about(self):
        Df_Dialog.MessageInfo("About", "Dragonfly Navigator " + Df.d.version + "\nCopyright 2017 Henrik Harmsen.\nLicense: GPLv3")
    
        
