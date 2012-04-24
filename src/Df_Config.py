from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df

class Config():
    def __init__(self):
        self.settings = QSettings("ISS", "Dragonfly Navigator")
    
    def load(self, configW):
        self.configW = configW
        pos = self.settings.value("pos", QPoint(100, 100))
        size = self.settings.value("size", QSize(400, 400))
#        Df.d.g.mw.resize(size)
#        Df.d.g.mw.move(pos)

        Df.d.bookmarks = self.settings.value("bookmarks", [ ])
        if type(Df.d.bookmarks) != type([]):
            Df.d.bookmarks = [ Df.d.bookmarks ]
        Df.d.lp.updateBookmarksMenu()
        Df.d.rp.updateBookmarksMenu()

        self.rememberStartDirs = bool(int(self.settings.value("rememberStartDirs", 1)))
        if self.rememberStartDirs:
            self.configW.rememberStartFolders.setChecked(True)
            self.configW.startAtSpecifiedFolders.setChecked(False)
        else:
            self.configW.rememberStartFolders.setChecked(False)
            self.configW.startAtSpecifiedFolders.setChecked(True)

        self.showHidden = int(self.settings.value("showHidden", int(Qt.Unchecked)))
        if self.showHidden == int(Qt.Checked):
            self.configW.showHidden.setCheckState(Qt.Checked)
        else:
            self.configW.showHidden.setCheckState(Qt.Unchecked)
        self.configW.showHidden.stateChanged.connect(self.showHiddenStateChanged)

        self.configW.useCurrentLeft.clicked.connect(self.useCurrentLeft)
        self.configW.useCurrentRight.clicked.connect(self.useCurrentRight)
        self.configW.buttonBox.accepted.connect(self.accepted)
        
        #self.configW.rememberStartFolders.clicked.connect(self.rememberStartFoldersClicked)
        #self.configW.startAtSpecifiedFolders.clicked.connect(self.startAtSpecifiedFoldersClicked)

        self.startDirLeft = self.settings.value("startDirLeft",'/')        
        self.startDirRight = self.settings.value("startDirRight",'/')        
        Df.d.lp.setPathByString(self.startDirLeft)
        Df.d.rp.setPathByString(self.startDirRight)
        self.configW.leftStartDir.setText(self.startDirLeft)
        self.configW.rightStartDir.setText(self.startDirRight)


    def accepted(self):
        self.save()
        Df.d.gb.refresh()
        
    def save(self):
        self.settings.setValue("pos", Df.d.g.mw.pos())
        self.settings.setValue("size", Df.d.g.mw.size())
        self.settings.setValue("bookmarks", Df.d.bookmarks)
        self.rememberStartDirs = self.configW.rememberStartFolders.isChecked()
        self.settings.setValue("rememberStartDirs", int(self.rememberStartDirs))
        if self.rememberStartDirs:
            self.settings.setValue("startDirLeft", Df.d.lp.cd.path())
            self.settings.setValue("startDirRight", Df.d.rp.cd.path())
        else:
            self.settings.setValue("startDirLeft", self.configW.leftStartDir.text())
            self.settings.setValue("startDirRight", self.configW.rightStartDir.text())
        self.showHidden = int(self.configW.showHidden.checkState())
        self.settings.setValue("showHidden", self.showHidden)
                 
    def useCurrentLeft(self):
        self.configW.leftStartDir.setText(Df.d.lp.cd.path())

    def useCurrentRight(self):
        self.configW.rightStartDir.setText(Df.d.rp.cd.path())
        
    def showHiddenStateChanged(self, state):
        self.showHidden = int(state)
