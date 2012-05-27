from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df

class Preview():
    def __init__(self, leftContainerW, rightContainerW, leftGvW, rightGvW, leftTextW, rightTextW, leftTreeW, rightTreeW):
        self.containerW = [0,0]
        self.gvW = [0,0]
        self.textW = [0,0]
        self.treeW = [0,0]
        self.containerW[0] = leftContainerW
        self.containerW[1] = rightContainerW
        self.gvW[0] = leftGvW
        self.gvW[1] = rightGvW
        self.textW[0] = leftTextW
        self.textW[1] = rightTextW
        self.treeW[0] = leftTreeW
        self.treeW[1] = rightTreeW
        self.scene = QtGui.QGraphicsScene()
        self.pixmap = None
        #self.size = self.gvW[0].size()

    def show(self, index, pm, text):
        (self.data, pixmap) = pm
        if index == 0:
            otherIndex = 1
        else:
            otherIndex = 0
        self.containerW[index].hide()
        self.containerW[otherIndex].show()
        self.treeW[otherIndex].hide()
        self.textW[otherIndex].setText(text)
        if self.pixmap:
            self.scene.clear()
        size = self.gvW[otherIndex].size()
        size = QSize(size.width()*0.95, size.height()*0.95)
        self.pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(self.pixmap)
        self.gvW[otherIndex].setScene(self.scene)
        
    def hide(self):
        self.containerW[0].hide()
        self.containerW[1].hide()
        self.treeW[0].show()
        self.treeW[1].show()

