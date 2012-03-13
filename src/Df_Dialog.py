from PySide.QtCore import *
from PySide import QtGui
import Df

def Dialog(title, instruction, prefill):    
    result, ok = QtGui.QInputDialog.getText(Df.d.g.mw, title, instruction, QtGui.QLineEdit.Normal, prefill)
    if ok and result != '':
        return result
    return None

def Message(title, text):
    QtGui.QMessageBox.warning(Df.d.g.mw, title, text, QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)