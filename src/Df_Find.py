from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df, time, hashlib, sys, string, thread
from Queue import Queue

class Find():
    def __init__(self, findW):
        self.findW = findW
        #self.findW.input.returnPressed.connect(self.startFind)
        self.findW.hitlist.header().hide()
        self.findW.hitlist.itemPressed.connect(self.itemClicked)
        self.findW.close.clicked.connect(self.close)
        self.findW.stop.clicked.connect(self.stopNow)
        self.findW.start.clicked.connect(self.startFind)
        self.findW.recursive.setCheckState(Qt.Checked)
        self.q = Queue()
        thread.start_new_thread(self.findTask, (self,))
        self.stop = False
        self.panel = None # While hidden this is none
        self.setSearchingFor("")

    def startFind(self):
        self.findW.hitlist.clear()
        cd = self.panel.cd
        t = self.findW.input.text()
        recurse = int(self.findW.recursive.checkState()) != 0
        self.q.put((self.panel.cd, t, recurse))

    def setSearchingFor(self, text):
        self.findW.currentSearch.setText("Searching: " + text)

    def findInNode(self, node, t, r):
        self.setSearchingFor(node.path())
        ch = node.children(False)
        for n in ch:
            if self.stop:
                return
            try:
                if string.find(n.name, t) != -1:
                    item = QtGui.QTreeWidgetItem( [ n.path() ] )
                    item.df_node = n
                    self.findW.hitlist.insertTopLevelItem(0, item)
            except:
                pass
            if not n.leaf() and r:
                self.findInNode(n, t, r)

    def findTask(self, dummy):
        try:
            while True:
                self.setStatus("Idle")
                self.stop = False
                cd,t,r = self.q.get(True)
                self.setStatus("Running")
                self.findInNode(cd, t, r)
        except:
            crash()
            
    def itemClicked(self, item):
        #print item.text(0)
        self.panel.setPathByString(item.df_node.parent.path())
        self.setHeader()
        self.panel.findMark = item.df_node.path()

    def setHeader(self):
        self.findW.heading.setText("Find in " + self.panel.cd.path() + "\nEnter part of object name to search for.")

    def show(self, panel):
        self.panel = panel
        self.setHeader()
        self.findW.input.clear()
        self.findW.hitlist.clear()
        self.findW.show()
        
    def close(self):
        self.stop = True
        self.findW.hide()
        
    def stopNow(self):
        self.stop = True

    def setStatus(self, status):
        self.findW.stop.setEnabled(status != "Idle")
        self.findW.start.setEnabled(status == "Idle")
        if status == "Idle":
            self.setSearchingFor("")
        self.findW.status.setText("Search engine: " + status)

