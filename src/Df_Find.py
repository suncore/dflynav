from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df, time, hashlib, sys, string, thread
from Queue import Queue

class Find():
    def __init__(self, findW):
        self.findW = findW
        self.findW.input.returnPressed.connect(self.startFind)
        self.findW.hitlist.header().hide()
        self.findW.hitlist.itemPressed.connect(self.itemClicked)
        self.q = Queue()
        thread.start_new_thread(self.findTask, (self,))
        self.stop = False
        self.panel = None # While hidden this is none

    def startFind(self):
        self.stop = True
        cd = self.panel.cd
        t = self.findW.input.text()
        recurse = int(self.findW.recursive.checkState()) != 0
        self.q.put((self.panel.cd, t, recurse))

    def findInNode(self, node, t, r):
        ch = node.children(False)
        for n in ch:
            if self.stop:
                return
            if string.find(n.name, t) != -1:
                item = QtGui.QTreeWidgetItem( [ n.path() ] )
                item.df_node = n
                self.findW.hitlist.insertTopLevelItem(0, item)
            if not n.leaf() and r:
                self.findInNode(n, t, r)

    def findTask(self, dummy):
        while True:
            self.setStatus("Idle")
            cd,t,r = self.q.get(True)
            self.setStatus("Running")
            self.findInNode(cd, t, r)
            self.stop = False

    def itemClicked(self, item):
        #print item.text(0)
        self.panel.setPath(item.df_node.parent)
        # TODO set selection on df_node
        self.setHeader()

    def setHeader(self):
        self.findW.heading.setText("Find in " + self.panel.cd.path() + "\nEnter part of object name to search for and press return.")

    def show(self, panel):
        self.panel = panel
        self.setHeader()
        self.findW.input.clear()
        self.findW.hitlist.clear()
        self.findW.show()

    def setStatus(self, status):
        self.findW.status.setText("Search engine: " + status)

