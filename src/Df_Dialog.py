from PySide.QtCore import *
from PySide import QtGui
import Df

def Dialog(title, instruction, prefill):    
    result, ok = QtGui.QInputDialog.getText(Df.d.g.mw, title, instruction, QtGui.QLineEdit.Normal, prefill)
    if ok and result != '':
        return result
    return None

def YesNo(title, text):    
    r = QtGui.QMessageBox.question(Df.d.g.mw, title, text, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
    return r == int(QtGui.QMessageBox.Ok)

def Message(title, text):
    QtGui.QMessageBox.warning(Df.d.g.mw, title, text, QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)