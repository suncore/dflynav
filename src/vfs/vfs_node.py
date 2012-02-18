import os
#from inspect import isclass
import Df

class Node(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.icon = None
        self.meta = [ ]
        self.children_ = None
        self.actionButtonCallbacks = []

    def leaf(self):
        return False

    def children(self):
        return self.children_
    
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

    def changed(self):
        return False

    def startMonitor(self, index):
        return
