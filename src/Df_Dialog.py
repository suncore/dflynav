from PyQt5.QtCore import *
from PyQt5 import QtGui
import Df, os, platform, subprocess, sys
from utils import *

def Dialog(title, instruction, prefill):    
    result, ok = QtWidgets.QInputDialog.getText(Df.d.g.mw, title, instruction, QtWidgets.QLineEdit.Normal, prefill)
    if ok and result != '':
        return result
    return None

def YesNo(title, text):    
    r = QtWidgets.QMessageBox.question(Df.d.g.mw, title, text, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)
    return r == int(QtWidgets.QMessageBox.Ok)

def MessageWarn(title, text):
    QtWidgets.QMessageBox.warning(Df.d.g.mw, title, text, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
    
def MessageInfo(title, text):
    QtWidgets.QMessageBox.information(Df.d.g.mw, title, text, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)

def TextDialog(title, text=None, file=None): 
    w = Df.d.g.help
    if not text:
        f = open(file)
        text = f.read()
        f.close()
    w.helpText.setHtml(text)
    w.setWindowTitle(title)
    w.show()
