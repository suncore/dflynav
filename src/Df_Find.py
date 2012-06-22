from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df, time, hashlib, sys, string

class Find():
    def __init__(self, findW):
        self.findW = findW
        self.findW.input.returnPressed.connect(self.find)
        self.findW.hitlist.header().hide()
        self.findW.hitlist.itemPressed.connect(self.itemClicked)

    def itemClicked(self, item):
        #print item.text(0)
        self.panel.setPath(item.df_node)

    def find(self):
        t = self.findW.input.text()
        cd = self.panel.cd
        ch = cd.children(False)
        for n in ch:
            if string.find(n.name, t) != -1:
                item = QtGui.QTreeWidgetItem( [ n.path() ] )
                item.df_node = n
                self.findW.hitlist.insertTopLevelItem(0, item)
                

    def reset(self):
        self.findW.heading.setText("Find in " + self.panel.cd.path() + "\nEnter part of object name to search for and press return.")
        self.findW.input.clear()
        self.findW.hitlist.clear()

    def show(self, panel):
        self.panel = panel
        self.reset()
        self.findW.show()

    def periodicRefresh(self):
        if self.waitingForChildren:
            if self.cd.childrenReady:
                self.waitingForChildren = False
                self.cd.childrenReady = False
                self.setPath2()
        else:
            if self.cd.changed:
                if not self.treeW.selectedItems():
                    self.cd.changed = False
                    self.refreshCd()
