from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df, time, hashlib, sys

class Find():
    def __init__(self, findW):
        self.findW = findW
        self.findW.input.returnPressed.connect(self.find)
        self.findW..header().hide()

    def find(self):
        self.panel.setPathByString(self.findW.input.text())

    def reset(self):
        self.findW.heading.setText("Find in " + self.panel.cd.path() + "\nEnter part of object name to search for and press return.")
        self.findW.input.clear()
        self.findW.hitlist.clear()

    def show(self, panel):
        self.panel = panel
        self.reset()
        self.findW.show()

