
import vfs, Df_Dialog
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
from utils import *
import Df
import os, subprocess, platform
from PIL import Image
import functools
from queue import Queue
import _thread

class PanelItem(QtWidgets.QTreeWidgetItem):
    # self.df_node is pointer to node that belongs to this item
    def __lt__(self, other):
        tw = self.treeWidget()
        col = tw.sortColumn()
        ln = self.df_node
        rn = other.df_node
        if col == 0: # File name column
            if ln.leaf() != rn.leaf():
                if ln.leaf():
                    return False
                else:
                    return True
            return ln.name_low < rn.name_low
        else:
            # if not tw.df_panel.refreshLocked:
            #     tw.df_panel.refreshLocked = True
            #     tw.df_panel.updateStatus()
            try:
                (_, _, lv) = ln.meta[col-1]
                (_, _, rv) = rn.meta[col-1]
                if lv == rv:
                    return ln.name_low < rn.name_low
                if col == 2 or col == 1 or col == 5: # Time and size should be sorted most recent first
                    return lv > rv
                else:
                    return lv < rv
            except:
                pass
            return True

def PanelIconQueueTask(dummy):
    while True:
        (pi, i) = Df.d.panelIconQueue.get(True)
        try:
            pi.setIcon(0, i.icon(fast=True)) # If panel item has been deleted, this will raise an exception and we won't spend time on jpeg thumb loading
            pi.setIcon(0, i.icon(fast=False))
        except:
            pass



class Panel(object):
    def __init__(self, mainW, treeW, pathW, statusW, upW, actionButtons, index, mirrorW, historyW, bookmarksW, backW, findW, terminalW):
        treeW.df_panel = self
        self.mainW = mainW
        self.treeW = treeW
        self.pathW = pathW
        self.upW = upW
        self.statusW = statusW
        self.findW = findW
        self.terminalW = terminalW
        self.other = None # Pointer to the other panel filled in by the builder
        self.treeW.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.actionButtons = actionButtons
        self.panelIdx = index
        f = self.treeW.font()
        ps = self.treeW.font().pointSize()
        f.setPointSize(ps * 1.1)
        ##print("pointsize",self.statusW.height())
        ##f.setBold(True)
        self.treeW.setFont(f)
        self.pathW.setFont(f)
        self.waitingForChildren = False
        self.mirrorW = mirrorW
        self.historyW = historyW
        self.bookmarksW = bookmarksW
        self.historyMenu = QtWidgets.QMenu(self.mainW)
        self.bookmarksMenu = QtWidgets.QMenu(self.mainW)
        self.cd = vfs.vfs_fs.Directory(None, '/', '/') # vfs.vfs_root.VfsRoot()
        self.historyW.setMenu(self.historyMenu)
        self.bookmarksW.setMenu(self.bookmarksMenu)
        self.bookmarksMenu.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bookmarksMenu.customContextMenuRequested.connect(self.bookmarksContextMenuPopup)
        self.bookmarksContextMenu = QtWidgets.QMenu(self.mainW)
        self.bookmarksContextMenu.addAction(QtWidgets.QAction('Delete', self.mainW, triggered = self.bookmarksContextMenuDelete))
        self.bookmarksMenuHoverPath = None
        self.refreshLocked = False
        self.backHistory = ['/']
        self.backW = backW
        self.treeW_noClear = False
        self.hoverItem = None
        self.hovering = False
        self.defaultIconSize = self.treeW.iconSize()
        self.controlMod = False
        self.hoverOldOppositeFolder = None
        self.findW.clicked.connect(self.find)
        self.findMark = None
        self.terminalW.clicked.connect(self.terminal)
        self.sortColumn = 0
        # self.treeW.header().setClickable(True)
        # self.treeW.header().clicked.connect(self.treeWheaderClicked)
        self.treeW.sortItems(0,Qt.AscendingOrder)

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
        self.treeW_leaveEventOrig = self.treeW.leaveEvent
        self.treeW.leaveEvent = self.treeW_leaveEvent
        self.treeW_keyPressEventOrig = self.treeW.keyPressEvent
        self.treeW.keyPressEvent = self.treeW_keyPressEvent
        self.treeW_keyReleaseEventOrig = self.treeW.keyReleaseEvent
        self.treeW.keyReleaseEvent = self.treeW_keyReleaseEvent
        self.treeW_mouseMoveEventOrig = self.treeW.mouseMoveEvent
        self.treeW.mouseMoveEvent = self.treeW_mouseMoveEvent
#        self.treeW.viewport().setMouseTracking(True)
#        self.treeW_mousePressEventOrig = self.treeW.viewport().mousePressEvent
#        self.treeW.viewport().mousePressEvent = self.treeW_mousePressEvent
        self.upW.clicked.connect(self.upW_clicked)
        self.backW.clicked.connect(self.backW_clicked)
        self.treeW.setSortingEnabled(True)
        #self.treeW.itemSelectionChanged.connect(self.treeW_selectionChanged)
        self.mirrorW.clicked.connect(self.mirrorW_clicked)
        self.pathW.returnPressed.connect(self.pathW_returnPressed)
        
    # Signal handlers ----------------------------------------------------------------------------------

    def find(self):
        Df.d.find.show(self)

    def terminal(self):
        error = None
        try:
            subprocess.Popen(["konsole","--workdir",self.cd.fspath]) 
        except:
            t,error,tb = sys.exc_info()
        if error:
            error = str(error)
        Df.d.jobm.addJobDone("$ konsole --workdir "+self.cd.fspath, error)
      
    def pathW_returnPressed(self):
        self.unlockRefresh()
        text = self.pathW.text()
        text = text.rstrip('/ ')
        c = self.setPathByString(text, False, False, True)
        if c:
            self.setPath(c)
        else:
            text = Df_Dialog.Dialog("Create directory?", "Could not find this directory. Do you want to create it?                                                                                                                              ", 
                                       text)
            if text:
                head = text.split('/')[:-1]
                head = '/'.join(head)
                tail = text.split('/')[-1:][0]
                c = self.setPathByString(head, False, False, True)
                if not c:
                    Df_Dialog.MessageWarn("Could not find parent directory", 'Could not find the parent directory\n"' + head + '"\nto create directory\n"' + tail + '"\nin.')
                    self.refreshCd()
                    return
                c.mkdir(tail)
            else:
                self.refreshCd()

    def mirrorW_clicked(self):
        self.setPathByString(self.other.cd.path())
    
    def treeW_pressed(self, item):
        buttons = QtWidgets.QApplication.mouseButtons()        # buttons can be Left-,Right-,Mid-Button
        if buttons == Qt.RightButton:
            self.openItem(item)

    def treeW_doubleClicked(self, item):
        self.openItem(item)

#    def treeW_activated(self, item):
#        i = self.treeW.itemAt(item.treeWidget().mapFromGlobal(QtWidgets.QCursor.pos()))
#        print "Item activated", item, i
#        if i:
#            print i.df_node.fspath
            
    def treeW_leaveEvent(self, e):
        #print "leave"
        self.stopMods()
        #self.treeW_leaveEventOrig(e)
            
    def treeW_keyPressEvent(self, e):
        if e.key() == Qt.Key_Alt:
            self.hovering = True
            self.hoverOldOppositeFolder = self.other.cd
            self.preview()
        elif e.key() == Qt.Key_Control:
            self.controlMod = True
        self.treeW_keyPressEventOrig(e)
            
    def treeW_keyReleaseEvent(self, e):
        self.stopMods()
        #self.treeW_keyReleaseEventOrig(e)
            
    def stopMods(self):
        Df.d.preview.hide()
        self.hovering = False
        self.hoverItem = None
        if self.hoverOldOppositeFolder:
            self.other.setPath(self.hoverOldOppositeFolder)
        self.hoverOldOppositeFolder = None
        self.controlMod = False

    def treeW_mouseMoveEvent(self, e):
        self.treeW.setFocus()
        if self.hovering:
            self.preview()
        self.treeW_mouseMoveEventOrig(e)

    def treeW_mousePressEvent(self, e):
        self.treeW_mousePressEventOrig(e)

    def preview(self):
        pos = QtGui.QCursor.pos() # e.globalPos()) in mouseMoveEvent
        i = self.treeW.itemAt(self.treeW.viewport().mapFromGlobal(pos))
        if not i:
            return
        n = i.df_node
        if i and i is not self.hoverItem:
            if not n.leaf():
                if n.linkTarget:
                    self.other.setPathByString(n.linkTarget)
                else:
                    self.other.setPath(n)
            else:
                qv = n.preview()
                if qv:
                    Df.d.preview.show(self.panelIdx, qv)
            self.hoverItem = i

    def openItem(self, item):
        self.other.treeW.clearSelection()
        node = item.df_node
        if node.leaf():
            node.open()
        else:
            s = self
            if self.controlMod:
                s = self.other
            if node.linkTarget:
                s.setPathByString(node.linkTarget)
                return
            s.setPath(node)

    def upW_clicked(self):
        if self.cd.parent:
            self.setPath(self.cd.parent)

    def backW_clicked(self):
        while self.backHistory[0] == self.cd.path() and len(self.backHistory) > 1:
            self.backHistory = self.backHistory[1:]
        path = self.backHistory[0]
        self.setPathByString(path, True, False)

    def setPathByString(self, path, bestEffort = True, addToBackHistory = True, searchOnly = False):
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
        if not searchOnly:
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
                if not self.refreshLocked:
                    self.cd.changed = False
                    self.refreshCd()

    def setPath(self, node, addToBackHistory = True):
        self.sortColumn = self.treeW.sortColumn()
        self.sortOrder = self.treeW.header().sortIndicatorOrder()
        # i = self.treeW.header().sortIndicatorSection()
        # print(self.sortColumn,self.sortOrder,i)
        # print(self.sortColumn)
        self.refreshLocked = False
        changed = False
        self.verticalPosition = None
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
        else:
            # Make sure we display at the same location as before in the vertical scroll in the panel
            self.verticalPosition = self.treeW.itemAt(QPoint(0,0))
            # try:
            #     print(self.verticalPosition.df_node.fspath)
            # except:
            #     pass
        self.cd = node
        self.cd.changed = False
        self.waitingForChildren = True
        self.pathW.setText(self.cd.path())
        self.setStatus(0,0)
        self.cd.startGetChildren()
        #self.treeW.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        #self.firstSectionWidth = self.treeW.header().sectionSize(0)

    def setPath2(self):
        #self.pathW.setText(self.cd.path())
        bigIcons = 0
        smallIcons = 0
        self.cd.startMonitor(self.panelIdx)
        ch = self.cd.children()
        keys = [ 'Name' ]
        self.treeW.setColumnCount(0)
        if ch:
            mastermeta = ch[0].meta
            metalen = 0
            for i in ch:
                l = len(i.meta)
                if metalen < l:
                    mastermeta = i.meta
                    metalen = l
            k = [ k for (k,s,v) in mastermeta ]
            keys = keys + k
        self.treeW.setHeaderLabels(keys)
        #w = 
        #print self.treeW.header().sectionSizeFromContents(0)
#        self.treeW.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
#        w = self.treeW.header().sectionSize(0)
#        print 'width'+str(w)

        #self.treeW.header().resizeSection(0, self.firstSectionWidth)
        #self.treeW.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)

        #w = self.treeW.header().viewport().width()
        #print w
        
        #self.treeW.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        items = []
        self.nrItems = 0
        findItem = None
        scrollToPi = None
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
                if type(1) == type(v):
                    pi.setTextAlignment(col, Qt.AlignCenter | Qt.AlignRight)
                col += 1
            pi.setIcon(0, i.icon(fast=True))
            if type(i).__name__ == "PictureFile":
                Df.d.panelIconQueue.put((pi,i))
            pi.df_node = i
            if self.findMark:
                if not findItem and self.findMark == i.path():
                    findItem = pi
            items.append(pi)
            self.nrItems += 1
            if i.bigIcon:
                bigIcons += 1
            else:
                smallIcons += 1
            try:
                if self.verticalPosition.df_node.fspath == i.fspath:
                    scrollToPi = pi
            except:
                pass
        self.treeW.clearSelection()
        self.treeW.clear()
        if bigIcons > smallIcons:
            self.treeW.setIconSize(QSize(64,64)) # was 40,40
        else:
            # print(self.defaultIconSize)
            # self.treeW.setIconSize(self.defaultIconSize)
            self.treeW.setIconSize(QSize(20,20)) 
        self.setActionButtons(items)
        self.treeW.insertTopLevelItems(0, items)
        self.treeW.sortItems(self.sortColumn,self.sortOrder) #Qt.AscendingOrder)
        # print(self.sortColumn)
        #self.treeW.resizeColumnToContents(1)
        self.treeW.header().setStretchLastSection(False)
        self.highestCol = len(keys)
        for col in range(1,self.highestCol):
            #self.treeW.header().setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)
            self.treeW.header().setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents) # TODO problematic
        self.setStatus(0, self.nrItems, 0, self.cd.fsFree())
        
        for i in range(len(keys)):
            if i > 2:
                self.treeW.header().hideSection(i)
        self.treeW.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch) 
        firstSectionWidth = self.treeW.header().sectionSize(0)
        self.treeW.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive) 
        self.treeW.header().resizeSection(0, firstSectionWidth*.96)
        for i in range(len(keys)):
            if i > 2:
                self.treeW.header().showSection(i)
        if findItem:
            self.treeW.scrollToBottom() 
            self.treeW.scrollToItem(findItem)
            self.treeW.setCurrentItem(findItem)
            self.findMark = None
        # lastPi = self.treeW.itemAt(QPoint(0,0))
        elif scrollToPi:
            self.treeW.scrollToBottom() 
            self.treeW.scrollToItem(scrollToPi)
                 
    def treeW_clearSelection(self):
        if not self.treeW_noClear:
            self.treeW.clearSelection()
                    
    def treeW_selectionChanged(self):
        self.treeW_noClear = True
        self.other.treeW_clearSelection()
        self.treeW_noClear = False
        s = self.treeW.selectedItems()
        if s:
            self.refreshLocked = True
        self.setActionButtons(s)
        sum = 0
        for i in s:
            if i.df_node:
                sum += i.df_node.size
        self.setStatus(len(s), self.nrItems, sum, self.cd.fsFree())

    def unlockRefresh(self):        
        self.refreshLocked = False
        self.other.refreshLocked = False

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
        def abcb(fun):
            self.unlockRefresh()
            fun()
        for i in cblist:
            name, binary, callback = i
            #cb = lambda func=callback: abcb(func)
            cb = functools.partial(abcb, fun=callback)
            if binary and s[0].df_node.binaryOpCompat(self.other.cd):
                self.actionButtons.addButton(name, cb)
            elif not binary:
                self.actionButtons.addButton(name, cb)

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
        self.statusdata = (selectedItems, totalItems, selectedSize, freeFileSystemSize)
        self.updateStatus()
        
    def updateStatus(self):
        selectedItems, totalItems, selectedSize, freeFileSystemSize = self.statusdata
        if freeFileSystemSize:
            self.statusW.setText("%d/%d = %s   Free: %s%s" % (selectedItems, totalItems, size2str(selectedSize), size2str(freeFileSystemSize), iff(self.refreshLocked,"  (Updates paused)","")))
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
            action = QtWidgets.QAction(path, self.mainW)
            #receiver = lambda path=path: self.gotoPath(path)
            receiver = functools.partial(self.gotoPath, path=path)
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
        action = QtWidgets.QAction('Add bookmark (right click on item to remove)', self.mainW)
        action.triggered.connect(self.addBookmark)
        actions.append(action)
        action = QtWidgets.QAction('', self.mainW)
        action.setSeparator(True)
        actions.append(action)
        for path in Df.d.bookmarks:
            action = QtWidgets.QAction(path, self.mainW)
            #receiver = lambda path=path: self.gotoPath(path)
            receiver = functools.partial(self.gotoPath, path=path)
            action.triggered.connect(receiver)
            #hover = lambda path=path: self.bookmarksMenuHoverPathSet(path)
            hover = functools.partial(self.bookmarksMenuHoverPathSet, path=path)
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
            
            
