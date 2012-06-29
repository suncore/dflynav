import os
#from inspect import isclass
import Df

class Node(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.name_low = name.lower()
        self.meta = [ ]
        self.children_ = []
        self.actionButtonCallbacks = []
        self.childrenReady = True
        self.changed = False
        self.size = 0
        self.linkTarget = None
        self.bigIcon = False

    def icon(self):
        return Df.d.iconFactory.getFolderIcon()

    def leaf(self):
        return False
    
    def open(self):
        pass

    def startGetChildren(self):
        self.childrenReady = True
        Df.d.refresh.refreshSig.emit()


    def children(self, async=True):
        return self.children_

    def childrenStop(self):
        pass
    
    def childByName(self, name):
        for c in self.children():
            if name == c.name:
                return c
        return None
    
    def path(self):
        n = self
        if n.name != None and n.name != '/':
            path = n.name
        else:
            path = ''
        n = n.parent
        while n:
            if path != '' and n.name != '/':
                path = n.name + '/' + path
            n = n.parent
        return '/' + path
    
    def binaryOpCompat(self, obj):
        return False

    def getSelectionAndDestination(self):
        return Df.d.lp.getSelectionAndDestination()

    def startMonitor(self, index):
        return
    
    def mkdir(self):
        pass
    
    def fsFree(self):
        return None
    
    def preview(self):
        return None

