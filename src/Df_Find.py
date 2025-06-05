from PyQt6.QtCore import *
from PyQt6 import QtGui, QtWidgets
from utils import *
import Df, time, hashlib, sys, string, _thread
from queue import Queue

class Communicate(QObject):
    signal = pyqtSignal()


class Find():
    def __init__(self, findW):
        self.findW = findW
        #self.findW.input.returnPressed.connect(self.startFind)
        self.findW.hitlist.header().hide()
        self.findW.hitlist.itemPressed.connect(self.itemClicked)
        self.findW.close.clicked.connect(self.close)
        self.findW.stop.clicked.connect(self.stopNow)
        self.findW.start.clicked.connect(self.startFind)
        self.findW.recursive.setCheckState(Qt.CheckState.Checked)
        self.q = Queue()
        self.q_sf = Queue()
        self.q_st = Queue()
        self.q_res = Queue()
        self.stop = False
        self.panel = None # While hidden this is none
        self.c = Communicate()
        self.c.signal.connect(self.addSearchResult)
        self.c_sf = Communicate()
        self.c_sf.signal.connect(self.setSearchingFor2)
        self.c_st = Communicate()
        self.c_st.signal.connect(self.setStatus2)
        _thread.start_new_thread(self.findTask, (self,))
        self.setSearchingFor("")

    def startFind(self):
        self.findW.hitlist.clear()
        cd = self.panel.cd
        t = self.findW.input.text()
        recurse = self.findW.recursive.isChecked()
        self.q.put((self.panel.cd, t, recurse))

    def setSearchingFor(self, text):
        self.q_sf.put(text)
        self.c_sf.signal.emit()

    def setSearchingFor2(self): # Runs in GUI thread
        text = self.q_sf.get(True)
        self.findW.currentSearch.setText("Searching: " + text)

    def findInNode(self, node, t, r):
        t = t.lower() #string.lower(t)
        self.setSearchingFor(node.path())
        ch = node.children(False)
        for n in ch:
            if self.stop:
                return
            if True: #try:
                name = n.name.lower() #string.lower(n.name)
                if name.find(t) != -1:
                    #item = QtWidgets.QTreeWidgetItem( [ n.path() ] )
                    #item.df_node = n
                    self.q_res.put(n)
                    self.c.signal.emit()
                    #self.findW.hitlist.insertTopLevelItem(0, item)
            #except:
                #pass
            if not n.leaf() and r:
                self.findInNode(n, t, r)

    def addSearchResult(self): # Runs in GUI thread
        n = self.q_res.get(True)
        item = QtWidgets.QTreeWidgetItem( [ n.path() ] )
        item.df_node = n
        self.findW.hitlist.insertTopLevelItem(0, item)

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
        self.findW.heading.setText("Search in " + self.panel.cd.path() + "\nEnter part of a file or directory name to search for. Search is case insensitive.")

    def show(self, panel):
        self.panel = panel
        self.setHeader()
        self.findW.input.clear()
        self.findW.hitlist.clear()
        self.findW.show()
        self.findW.input.setFocus()

    def close(self):
        self.stop = True
        self.findW.hide()
        
    def stopNow(self):
        self.stop = True

    def setStatus(self, status):
        self.q_st.put(status)
        self.c_st.signal.emit()
        
    def setStatus2(self): # Runs in GUI thread
        status = self.q_st.get(True)
        self.findW.stop.setEnabled(status != "Idle")
        self.findW.start.setEnabled(status == "Idle")
        if status == "Idle":
            self.setSearchingFor("")
        self.findW.status.setText("Search engine: " + status)

