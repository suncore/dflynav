
import vfs, Df_Dialog
from PySide.QtCore import *
from PySide import QtGui
from utils import *


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
            return ln.name < rn.name 
        else:
            (lk, ls, lv) = self.df_node.meta[col-1]
            (rk, rs, rv) = other.df_node.meta[col-1]
            return lv < rv 

class Panel():
    def __init__(self, treeW, pathW, statusW, upW, actionButtons, index, mirrorW):
        self.treeW = treeW
        self.pathW = pathW
        self.upW = upW
        self.statusW = statusW
        self.other = None # Pointer to the other panel filled in by the builder
        self.treeW.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.actionButtons = actionButtons
        self.panelIdx = index
        #self.fileIcon = QtGui.QIcon(QtGui.QPixmap(':/icons/File.png'))
        self.fileIcon = self.treeW.style().standardIcon(QtGui.QStyle.SP_FileIcon)
        #self.folderIcon = QtGui.QIcon(QtGui.QPixmap(':/icons/Folder.png'))
        self.folderIcon = self.treeW.style().standardIcon(QtGui.QStyle.SP_DirIcon)
        self.waitingForChildren = False
        self.mirrorW = mirrorW
        
    def start(self):
        self.cd = vfs.vfs_root.VfsRoot()
        self.refreshCd()
        #self.treeW.pressed.connect(self.treeW_pressed)
        self.treeW.itemPressed.connect(self.treeW_pressed)
        self.treeW.itemSelectionChanged.connect(self.treeW_selectionChanged)
        self.upW.clicked.connect(self.upW_clicked)
        self.treeW.setSortingEnabled(True)
        #self.treeW.itemSelectionChanged.connect(self.treeW_selectionChanged)
        self.mirrorW.clicked.connect(self.mirrorW_clicked)
        self.pathW.returnPressed.connect(self.pathW_returnPressed)

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

    # Signal handlers
    def mirrorW_clicked(self):
        self.setPath(self.other.cd)
    
    def treeW_pressed(self, item):
        self.other.treeW.clearSelection()
        buttons = QtGui.QApplication.mouseButtons()        # buttons can be Left-,Right-,Mid-Button
        if buttons == Qt.RightButton:
            node = item.df_node
            if not node.leaf():
                self.setPath(node)
        else:
            self.leftMouseButton()

    def upW_clicked(self):
        if self.cd.parent:
            self.setPath(self.cd.parent)

    def setPathByString(self, path, bestEffort = True):
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
        self.setPath(c)
        return c

    def refreshCd(self):
        self.setPath(self.cd)

    def periodicRefresh(self):
        if self.waitingForChildren:
            if self.cd.childrenReady:
                self.waitingForChildren = False
                self.cd.childrenReady = False
                self.setPath2()
                #print "got children for " + self.cd.name
        else:
            if self.cd.changed and not self.treeW.selectedItems():
                self.cd.changed = False
                self.refreshCd()
            #print "reacting to change for " + self.cd.name

    def setPath(self, node):
        #print "setpath" + node.path()
        if node != self.cd:
            self.cd.childrenStop()
            self.treeW.clearSelection()
            self.treeW.clear() #TODO show hourglass
            item = PanelItem([ 'Loading...'])
            item.df_node = None
            self.treeW.insertTopLevelItems(0, [item])
        self.cd = node
        self.cd.changed = False
        self.cd.startGetChildren()
        self.waitingForChildren = True
        self.pathW.setText(self.cd.path())
        self.setStatus(0,0)

    def setPath2(self):
        #self.pathW.setText(self.cd.path())
        self.cd.startMonitor(self.panelIdx)
        ch = self.cd.children()
        keys = [ 'Name' ]
        self.treeW.setColumnCount(0)
        if ch:
            k = [ k for (k,s,v) in ch[0].meta ]
            keys = keys + k
        self.treeW.setHeaderLabels(keys)
        self.treeW.header().setResizeMode(0, QtGui.QHeaderView.Stretch)
        items = []
        self.nrItems = 0
        for i in ch:
            item  = [ i.name ]
            for k,s,v in i.meta:
                item.append(s)
            pi = PanelItem(item)
            col = 1
            for k,s,v in i.meta:
                if type(1L) == type(v):
                    pi.setTextAlignment(col, Qt.AlignCenter | Qt.AlignRight)
                col += 1
            if i.leaf():
                #pi.setIcon(0, self.treeW.style().standardIcon(QtGui.QStyle.SP_FileIcon))
                pi.setIcon(0, self.fileIcon)
            else:
                #pi.setIcon(0, self.treeW.style().standardIcon(QtGui.QStyle.SP_DirIcon))
                pi.setIcon(0, self.folderIcon)
            #pi.setIcon(0, QtGui.QIcon(QtGui.QPixmap(':/images/textpointer.png')))
            #pi.setData(QtCore.Qt.UserRole, pixmap)
            pi.df_node = i
            items.append(pi)
            self.nrItems += 1
        self.treeW.clearSelection()
        self.treeW.clear()
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
        self.setStatus(0,self.nrItems, 0, self.cd.fsFree())
                
    def leftMouseButton(self):
        pass
    
    def treeW_selectionChanged(self):
        s = self.treeW.selectedItems()
        self.setActionButtons(s)
        self.setStatus(len(s), self.nrItems, 0, self.cd.fsFree())
        
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
            self.statusW.setText("%d/%d = %s  Free: %s" % (selectedItems, totalItems, size2str(selectedSize), size2str(freeFileSystemSize)))
        else:
            self.statusW.setText("%d/%d" % (selectedItems, totalItems))
