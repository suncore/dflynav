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
        self.scene = [0,0]
        self.item = [0,0]

        self.containerW[0] = leftContainerW
        self.containerW[1] = rightContainerW
        self.gvW[0] = leftGvW
        self.gvW[1] = rightGvW
        self.gvW[0].origresizeEvent = self.gvW[0].resizeEvent
        self.gvW[1].origresizeEvent = self.gvW[1].resizeEvent
        self.gvW[0].resizeEvent = self.gvW_resizeEvent0
        self.gvW[1].resizeEvent = self.gvW_resizeEvent1
        self.gvW[1] = rightGvW
        self.textW[0] = leftTextW
        self.textW[1] = rightTextW
        self.treeW[0] = leftTreeW
        self.treeW[1] = rightTreeW
        self.scene[0] = QtGui.QGraphicsScene()
        self.scene[1] = QtGui.QGraphicsScene()
        self.gvW[0].setScene(self.scene[0])
        self.gvW[1].setScene(self.scene[1])
        #self.size = self.gvW[0].size()

    def gvW_resizeEvent0(self, event):
        self.gvW[0].fitInView(self.item[0], Qt.KeepAspectRatio)

    def gvW_resizeEvent1(self, event):
        self.gvW[1].fitInView(self.item[1], Qt.KeepAspectRatio)

    def show(self, index, qv):
        (pm, text) = qv
        (self.data, pixmap) = pm
        if index == 0:
            i = 1
        else:
            i = 0
        self.scene[i].clear()
        #size = self.gvW[i].size()
        #size = QSize(size.width()*0.95, size.height()*0.95)
        #self.pixmap = pixmap #pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.item[i] = self.scene[i].addPixmap(pixmap)
        self.gvW[i].fitInView(-2000,-2000,-1,-1)
        self.containerW[index].hide()
        self.containerW[i].show()
        self.treeW[i].hide()
        self.textW[i].setText(text)
        
    def hide(self):
        self.containerW[0].hide()
        self.containerW[1].hide()
        self.treeW[0].show()
        self.treeW[1].show()

