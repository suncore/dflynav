from PyQt6.QtCore import *
from PyQt6 import QtCore, QtGui, QtWidgets, QtWidgets
import Df, os, platform, subprocess, sys
from utils import *

def Dialog(title, instruction, prefill):    
    result, ok = QtWidgets.QInputDialog.getText(Df.d.g.mw, title, instruction, QtWidgets.QLineEdit.EchoMode.Normal, prefill)
    if ok and result != '':
        return result
    return None

def YesNo(title, text):    
    r = QtWidgets.QMessageBox.question(Df.d.g.mw, title, text, QtWidgets.QMessageBox.StandardButton.Ok, QtWidgets.QMessageBox.StandardButton.Cancel)
    return r == int(QtWidgets.QMessageBox.StandardButton.Ok)

def MessageWarn(title, text):
    QtWidgets.QMessageBox.warning(Df.d.g.mw, title, text, QtWidgets.QMessageBox.StandardButton.Ok, QtWidgets.QMessageBox.StandardButton.NoButton)
    
def MessageInfo(title, text):
    QtWidgets.QMessageBox.information(Df.d.g.mw, title, text, QtWidgets.QMessageBox.StandardButton.Ok, QtWidgets.QMessageBox.StandardButton.NoButton)

def TextDialog(title, text=None, file=None): 
    w = Df.d.g.help
    if not text:
        f = open(file)
        text = f.read()
        f.close()
    w.helpText.setHtml(text)
    w.setWindowTitle(title)
    w.show()
