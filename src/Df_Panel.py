
import vfs, Df_Dialog
from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df
import os, subprocess, platform
from PIL import Image

class PanelItem(QtGui.QTreeWidgetItem):
    # self.df_node is pointer to node that belongs to this item
    def __lt__(self, other):
        col = self.treeWidget().sortColumn()
        if col == 0:
            ln = self.df_node
            rn = other.df_node
            if ln.leaf() != rn.leaf():
                if ln.leaf():
                    return False
                else:
                    return True
            return ln.name_low < rn.name_low
        else:
            (lk, ls, lv) = self.df_node.meta[col-1]
            (rk, rs, rv) = other.df_node.meta[col-1]
            return lv < rv 


class Panel(object):
    def __init__(self, mainW, treeW, pathW, statusW, upW, actionButtons, index, mirrorW, historyW, bookmarksW, backW):
        self.mainW = mainW
        self.treeW = treeW
        self.pathW = pathW
        self.upW = upW
        self.statusW = statusW
        self.other = None # Pointer to the other panel filled in by the builder
        self.treeW.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.actionButtons = actionButtons
        self.panelIdx = index

        self.waitingForChildren = False
        self.mirrorW = mirrorW
        self.historyW = historyW
        self.bookmarksW = bookmarksW
        self.historyMenu = QtGui.QMenu(self.mainW)
        self.bookmarksMenu = QtGui.QMenu(self.mainW)
        self.cd = vfs.vfs_root.VfsRoot()
        self.historyW.setMenu(self.historyMenu)
        self.bookmarksW.setMenu(self.bookmarksMenu)
        self.bookmarksMenu.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bookmarksMenu.customContextMenuRequested.connect(self.bookmarksContextMenuPopup)
        self.bookmarksContextMenu = QtGui.QMenu(self.mainW)
        self.bookmarksContextMenu.addAction(QtGui.QAction('Delete', self.mainW, triggered = self.bookmarksContextMenuDelete))
        self.bookmarksMenuHoverPath = None
        self.backHistory = ['/']
        self.backW = backW
        self.treeW_noClear = False
        self.hoverItem = None
        self.hovering = False
        self.defaultIconSize = self.treeW.iconSize()
        
    def start(self):
        self.refreshCd()
        self.updateHistoryMenuBoth()
        self.updateBookmarksMenuBoth()
        #self.treeW.pressed.connect(self.treeW_pressed)
        self.treeW.itemPressed.connect(self.treeW_pressed)
        self.treeW.itemDoubleClicked.connect(self.treeW_doubleClicked)
        self.treeW.itemSelectionChanged.connect(self.treeW_selectionChanged)
        #self.treeW.itemActivated.connect(self.treeW_activated)
        self.treeW.setMouseTracking(True)
#        self.treeW_leaveEventOrig = self.treeW.leaveEvent
#        self.treeW.leaveEvent = self.treeW_leaveEvent
        self.treeW_keyPressEventOrig = self.treeW.keyPressEvent
        self.treeW.keyPressEvent = self.treeW_keyPressEvent
        self.treeW_keyReleaseEventOrig = self.treeW.keyReleaseEvent
        self.treeW.keyReleaseEvent = self.treeW_keyReleaseEvent
        self.treeW_mouseMoveEventOrig = self.treeW.mouseMoveEvent
        self.treeW.mouseMoveEvent = self.treeW_mouseMoveEvent
        self.upW.clicked.connect(self.upW_clicked)
        self.backW.clicked.connect(self.backW_clicked)
        self.treeW.setSortingEnabled(True)
        #self.treeW.itemSelectionChanged.connect(self.treeW_selectionChanged)
        self.mirrorW.clicked.connect(self.mirrorW_clicked)
        self.pathW.returnPressed.connect(self.pathW_returnPressed)
        
    # Signal handlers ----------------------------------------------------------------------------------
    def pathW_returnPressed(self):
        text = self.pathW.text()
        text = text.rstrip('/ ')
        c = self.setPathByString(text, False)
        if not c:
            text = Df_Dialog.Dialog("Create directory?", "Could not find this directory. Do you want to create it?                                                                                                                              ", 
                                       text)
            if text:
                head = text.split('/')[:-1]
                head = '/'.join(head)
                tail = text.split('/')[-1:][0]
                c = self.setPathByString(head, False)
                if not c:
                    Df_Dialog.Message("Could not find parent directory", 'Could not find the parent directory\n"' + head + '"\nto create directory\n"' + tail + '"\nin.')
                    self.refreshCd()
                    return
                c.mkdir(tail)
            else:
                self.refreshCd()

    def mirrorW_clicked(self):
        self.setPath(self.other.cd)
    
    def treeW_pressed(self, item):
        buttons = QtGui.QApplication.mouseButtons()        # buttons can be Left-,Right-,Mid-Button
        if buttons == Qt.RightButton:
            self.openItem(item)

    def treeW_doubleClicked(self, item):
        self.openItem(item)

#    def treeW_activated(self, item):
#        i = self.treeW.itemAt(item.treeWidget().mapFromGlobal(QtGui.QCursor.pos()))
#        print "Item activated", item, i
#        if i:
#            print i.df_node.fspath
            
#    def treeW_leaveEvent(self, e):
#        Df.d.preview.hide()
#        self.hovering = False
#        self.treeW_leaveEventOrig(e)
            
    def treeW_keyPressEvent(self, e):
        if e.key() == Qt.Key_Alt:
            self.hovering = True
            self.preview()
        self.treeW_keyPressEventOrig(e)
            
            
    def treeW_keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Alt:
            Df.d.preview.hide()
            self.hovering = False
            self.hoverItem = None
        self.treeW_keyReleaseEventOrig(e)
            

    def treeW_mouseMoveEvent(self, e):
        self.treeW.setFocus()
        if self.hovering:
            self.preview()
        self.treeW_mouseMoveEventOrig(e)

    def preview(self):
        pos = QtGui.QCursor.pos() # e.globalPos()) in mouseMoveEvent
        i = self.treeW.itemAt(self.treeW.viewport().mapFromGlobal(pos))
        if i and i is not self.hoverItem:
            qv = i.df_node.preview()
            if qv:
                Df.d.preview.show(self.panelIdx, qv)
            self.hoverItem = i

    def openItem(self, item):
        self.other.treeW.clearSelection()
        node = item.df_node
        if node.leaf():
            node.open()
        else:
            if node.linkTarget:
                self.setPathByString(node.linkTarget)
                return
            self.setPath(node)

    def upW_clicked(self):
        if self.cd.parent:
            self.setPath(self.cd.parent)

    def backW_clicked(self):
        while self.backHistory[0] == self.cd.path() and len(self.backHistory) > 1:
            self.backHistory = self.backHistory[1:]
        path = self.backHistory[0]
        self.setPathByString(path, True, False)

    def setPathByString(self, path, bestEffort = True, addToBackHistory = True):
        path = path.rstrip('/')
        c = self.cd
        while c.parent:
            c = c.parent
        for i in path.rsplit('/')[1:]:
            parent = c
            c = parent.childByName(i)
            if not c:
                if bestEffort:
                    c = parent
                    break
                else:
                    return None
        self.setPath(c, addToBackHistory)
        return c

    def refreshCd(self):
        self.setPath(self.cd)

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

    def setPath(self, node, addToBackHistory = True):
        changed = False
        if node != self.cd:
            self.updateHistoryMenuBoth()
            self.cd.childrenStop()
            self.treeW.clearSelection()
            self.treeW.clear() #TODO show hourglass
            item = PanelItem([ 'Loading...'])
            item.df_node = None
            self.treeW.insertTopLevelItems(0, [item])
            changed = True
            if addToBackHistory:
                self.backHistory.insert(0,node.path())
                self.backHistory = self.backHistory[0:100]
        self.cd = node
        self.cd.changed = False
        self.cd.startGetChildren()
        self.waitingForChildren = True
        self.pathW.setText(self.cd.path())
        self.setStatus(0,0)


    def setPath2(self):
        #self.pathW.setText(self.cd.path())
        bigIcons = 0
        smallIcons = 0
        self.cd.startMonitor(self.panelIdx)
        ch = self.cd.children()
        keys = [ 'Name' ]
        self.treeW.setColumnCount(0)
        if ch:
            metalen = 0
            for i in ch:
                l = len(i.meta)
                if metalen < l:
                    mastermeta = i.meta
                    metalen = l
            k = [ k for (k,s,v) in mastermeta ]
            keys = keys + k
        self.treeW.setHeaderLabels(keys)
        self.treeW.header().setResizeMode(0, QtGui.QHeaderView.Stretch)
        items = []
        self.nrItems = 0
        for i in ch:
            item  = [ i.name ]
            idx = 0
            for k,s,v in i.meta:
                k2,s2,v2 = mastermeta[idx]
                if k == k2:
                    item.append(s)
                else:
                    item.append('')
                idx += 1
            pi = PanelItem(item)
            col = 1
            for k,s,v in i.meta:
                if type(1L) == type(v):
                    pi.setTextAlignment(col, Qt.AlignCenter | Qt.AlignRight)
                col += 1
            pi.setIcon(0, i.icon())
            pi.df_node = i
            items.append(pi)
            self.nrItems += 1
            if i.bigIcon:
                bigIcons += 1
            else:
                smallIcons += 1
        self.treeW.clearSelection()
        self.treeW.clear()
        if bigIcons > smallIcons:
            self.treeW.setIconSize(QSize(40,40))
        else:
            self.treeW.setIconSize(self.defaultIconSize)
        self.setActionButtons(items)
        self.treeW.insertTopLevelItems(0, items)
        self.treeW.sortItems(0,Qt.AscendingOrder)
        #self.treeW.resizeColumnToContents(1)
        self.treeW.header().setStretchLastSection(False)
        self.highestCol = len(keys)
        col = 1
        for i in keys:
            self.treeW.header().setResizeMode(col, QtGui.QHeaderView.ResizeToContents)
            col += 1
        self.setStatus(0, self.nrItems, 0, self.cd.fsFree())
                 
    def treeW_clearSelection(self):
        if not self.treeW_noClear:
            self.treeW.clearSelection()
                    
    def treeW_selectionChanged(self):
        self.treeW_noClear = True
        self.other.treeW_clearSelection()
        self.treeW_noClear = False
        s = self.treeW.selectedItems()
        self.setActionButtons(s)
        sum = 0
        for i in s:
            sum += i.df_node.size
        self.setStatus(len(s), self.nrItems, sum, self.cd.fsFree())
        
    def setActionButtons(self, s):
        if not s:
            return
        self.actionButtons.clearButtons()
        if not s[0].df_node:
            return
        oldtype = type(s[0].df_node)
        cblist = s[0].df_node.actionButtonCallbacks
        for x in s[1:]:
            newtype = type(x.df_node)
            if oldtype == newtype:
                continue
            oldtype = newtype
            cblist2 = []
            for y in x.df_node.actionButtonCallbacks:
                name, binary, callback = y
                for z in cblist:
                    name2, binary2, callback2 = z
                    if name == name2:
                        cblist2.append(y)
                        break
            cblist = cblist2
        for i in cblist:
            name, binary, callback = i
            if binary and s[0].df_node.binaryOpCompat(self.other.cd):
                self.actionButtons.addButton(name, callback)
            elif not binary:
                self.actionButtons.addButton(name, callback)

    def getSelectionAndDestination(self):
        s1 = self.treeW.selectedItems()
        self.treeW.clearSelection()
        s2 = self.other.treeW.selectedItems()
        self.other.treeW.clearSelection()
        if s1:
            dest = self.other.cd
        else:
            dest = self.cd
        s = [x.df_node for x in s1+s2]
        return s, dest

    def setStatus(self, selectedItems, totalItems, selectedSize = None, freeFileSystemSize = None):
        if freeFileSystemSize:
            self.statusW.setText("%d/%d = %s   Free: %s" % (selectedItems, totalItems, size2str(selectedSize), size2str(freeFileSystemSize)))
        else:
            self.statusW.setText("%d/%d" % (selectedItems, totalItems))

    def gotoPath(self, path):
        self.setPathByString(path, True)

    def updateHistoryMenuBoth(self):
        self.updateHistoryMenu(True)
        self.other.updateHistoryMenu(False)

    def updateHistoryMenu(self, rebuildHistory = True):
        path = self.cd.path()
        h = Df.d.history
        if rebuildHistory:
            for i in range(0,len(h)):
                if h[i] == path:
                    h = [path] + h[:i] + h[i+1:]
                    break
            else:
                h.insert(0, path)
            Df.d.history = h[:30]
        self.historyMenu.clear()
        actions = []
        for path in h:
            action = QtGui.QAction(path, self.mainW)
            receiver = lambda path=path: self.gotoPath(path)
            action.triggered.connect(receiver)
            actions.append(action)
        self.historyMenu.addActions(actions)

    def updateBookmarksMenuBoth(self):
        self.updateBookmarksMenu()
        self.other.updateBookmarksMenu()

    def addBookmark(self):
        path = self.cd.path()
        h = Df.d.bookmarks
        for i in range(0,len(h)):
            if h[i] == path:
                h = [path] + h[:i] + h[i+1:]
                break
        else:
            h.append(path)
        Df.d.bookmarks = h
        Df.d.config.save()
        self.updateBookmarksMenuBoth()
        
    def updateBookmarksMenu(self):
        self.bookmarksMenu.clear()
        actions = []
        action = QtGui.QAction('Add bookmark', self.mainW)
        action.triggered.connect(self.addBookmark)
        actions.append(action)
        action = QtGui.QAction('', self.mainW)
        action.setSeparator(True)
        actions.append(action)
        for path in Df.d.bookmarks:
            action = QtGui.QAction(path, self.mainW)
            receiver = lambda path=path: self.gotoPath(path)
            action.triggered.connect(receiver)
            hover = lambda path=path: self.bookmarksMenuHoverPathSet(path)
            action.hovered.connect(hover)
            actions.append(action)
        self.bookmarksMenu.addActions(actions)

    def bookmarksContextMenuPopup(self, point):
        self.bookmarksContextMenu.exec_(self.bookmarksMenu.mapToGlobal(point))        

    def bookmarksMenuHoverPathSet(self, path):
        self.bookmarksMenuHoverPath = path
        
    def bookmarksContextMenuDelete(self):
        if self.bookmarksMenuHoverPath != None:
            path = self.bookmarksMenuHoverPath
            h = Df.d.bookmarks
            for i in range(0,len(h)):
                if h[i] == path:
                    h = h[:i] + h[i+1:]
                    break
            Df.d.bookmarks = h
            self.updateBookmarksMenuBoth()
            
            