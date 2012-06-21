from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df, time, hashlib, sys

class Find():
    def __init__(self, findW):
        self.findW = findW
        self.findW.find.clicked.connect(self.find)

    def find(self):
        pass

    def clear(self):
        self.findW.input.clear()

    def show(self):
        self.clear()
        self.findW.show()
