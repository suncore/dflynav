
from PyQt6.QtCore import *
from PyQt6 import QtGui
from utils import *
import Df
        
class Mainwin(object):
    def __init__(self, mainW, leftPanel, rightPanel):
        self.mainW = mainW
        self.mainW_keyPressEventOrig = self.mainW.keyPressEvent
        self.mainW.keyPressEvent = self.mainW_keyPressEvent

    
    def mainW_keyPressEvent(self, e):
        print(e)
        self.mainW_keyPressEventOrig(e)

