from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
from utils import *
import Df

class Preview():
    def __init__(self, leftContainerW, rightContainerW, leftGvW, rightGvW, leftTextW, rightTextW, leftTreeW, rightTreeW, leftTextBrowserW, rightTextBrowserW):
        self.containerW = [0,0]
        self.gvW = [0,0]
        self.textW = [0,0]
        self.treeW = [0,0]
        self.scene = [0,0]
        self.item = [None, None]
        self.data = [0,0]
        self.pixmap = [0,0]
        self.textBrowserW = [0,0]

        self.containerW[0] = leftContainerW
        self.containerW[1] = rightContainerW
        self.gvW[0] = leftGvW
        self.gvW[1] = rightGvW
        self.textBrowserW[0] = leftTextBrowserW
        self.textBrowserW[1] = rightTextBrowserW

        #self.gvW[0].origresizeEvent = self.gvW[0].resizeEvent
        #self.gvW[1].origresizeEvent = self.gvW[1].resizeEvent
        self.gvW[0].resizeEvent = self.gvW_resizeEvent0
        self.gvW[1].resizeEvent = self.gvW_resizeEvent1
        self.gvW[0].showEvent = self.gvW_showEvent0
        self.gvW[1].showEvent = self.gvW_showEvent1
        self.textW[0] = leftTextW
        self.textW[1] = rightTextW
        self.treeW[0] = leftTreeW
        self.treeW[1] = rightTreeW
        self.scene[0] = QtWidgets.QGraphicsScene()
        self.scene[1] = QtWidgets.QGraphicsScene()
        self.gvW[0].setScene(self.scene[0])
        self.gvW[1].setScene(self.scene[1])
        #self.size = self.gvW[0].size()

    def gvW_resizeEvent0(self, event):
        self.reShow(0)
    def gvW_resizeEvent1(self, event):
        self.reShow(1)
    def gvW_showEvent0(self, event):
        self.reShow(0)
    def gvW_showEvent1(self, event):
        self.reShow(1)

    def reShow(self, i):
        #self.gvW[i].fitInView(100000,100000,1,1)
        if self.previewType == 'image' and self.pixmap[i]:
            #w = self.pixmap[i].width()
            #h = self.pixmap[i].height()
            #self.gvW[i].fitInView(w/2, h/2, 20,20, Qt.KeepAspectRatio)
            #self.gvW[i].fitInView(self.item[i], Qt.KeepAspectRatio)
            size = self.gvW[i].viewport().size() # TODO wrong when just exposed?
            vw = size.width()
            vh = size.height()
            pixmap = self.pixmap[i].scaled(QSize(vw,vh), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            size = pixmap.size()
            pw = size.width()
            ph = size.height()
            x = y = 0
            if vw > pw:
                x = -(vw-pw)/2
            if vh > ph:
                y = -(vh-ph)/2
            self.gvW[i].setSceneRect(QRectF(x,y,vw,vh))
            self.scene[i].clear()
            self.item[i] = self.scene[i].addPixmap(pixmap)
        elif self.previewType == 'text':
            pass

    def show(self, index, qv):
        qvtype, qvd = qv
        self.previewType = qvtype
        if qvtype == 'image':
            pm, text = qvd
            if index == 0:
                i = 1
            else:
                i = 0
            (self.data[i], self.pixmap[i]) = pm
            #self.containerW[index].hide()
            self.treeW[i].hide()
            self.containerW[i].show()
            self.textBrowserW[i].hide()
            self.textW[i].setText(text)
            #print self.pixmap[i].size()
            self.reShow(i)
        if qvtype == 'text':
            if index == 0:
                i = 1
            else:
                i = 0
            self.treeW[i].hide()
            self.containerW[i].hide()
            self.textBrowserW[i].show()
            self.textBrowserW[i].setText(qvd)
            self.reShow(i)
        
    def hide(self):
        self.containerW[0].hide()
        self.containerW[1].hide()
        self.treeW[0].show()
        self.treeW[1].show()
        self.textBrowserW[0].hide()
        self.textBrowserW[1].hide()

