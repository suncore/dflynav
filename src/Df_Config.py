from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df, time, hashlib, sys, Df_Dialog


class Config():
    def __init__(self):
        self.settings = QSettings("Dragonfly", "Dragonfly Navigator")
    
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

        s = "cm29sh5g9sxk24fg2.dr"
        self.s = s
        ikey = self.settings.value("ikey", "") # Installation time key
        if ikey == "":
            if Df.d.bookmarks != []:
                sys.exit(0) # Deleted key. No go.
            now = str(int(time.time()))
            h = hashlib.sha1(now+s).hexdigest()
            self.settings.setValue("ikey", now+','+h)
            Df.d.gb.help()
        else:
            a = ikey.split(',')
            h = hashlib.sha1(a[0]+s).hexdigest()
            if h != a[1]:
                Df_Dialog.MessageWarn("License", "Install key is invalid. Exiting.")
                sys.exit(0) # Hacked key. No go.

        Df.d.licenseKey = ""
        lkey = self.settings.value("lkey", "") # License key = email address + hash
        if lkey == "":
            ikey = self.settings.value("ikey", "") # Installation time key
            a = ikey.split(',')
            daysleft = 31-(time.time() - int(a[0]))/3600/24
            if daysleft < 0:
                Df_Dialog.MessageWarn("License", "Trial period has expired. Exiting.")
                sys.exit(0)
            self.licenseNag("License", "You have " + str(int(daysleft)) + " days left on the trial.")
        else:
            a = lkey.split(',')
            h = hashlib.sha1(a[0]+s).hexdigest()[0:8]
            if h != a[1]:
                Df_Dialog.MessageWarn("License", "License key is invalid. Exiting.")
                sys.exit(0) # Hacked registry key. No go.
            else:
                Df.d.licenseKey = lkey

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

        self.showThumbs = int(self.settings.value("showThumbs", int(Qt.Checked)))
        if self.showThumbs == int(Qt.Checked):
            self.configW.showThumbs.setCheckState(Qt.Checked)
        else:
            self.configW.showThumbs.setCheckState(Qt.Unchecked)
        self.configW.showThumbs.stateChanged.connect(self.showThumbsStateChanged)

        self.useInternalFileCopy = int(self.settings.value("useInternalFileCopy", int(Qt.Unchecked)))
        if self.useInternalFileCopy == int(Qt.Checked):
            self.configW.useInternalFileCopy.setCheckState(Qt.Checked)
        else:
            self.configW.useInternalFileCopy.setCheckState(Qt.Unchecked)
        self.configW.useInternalFileCopy.stateChanged.connect(self.useInternalFileCopyStateChanged)

        self.showIcons = int(self.settings.value("showIcons", int(Qt.Unchecked)))
        if self.showIcons == int(Qt.Checked):
            self.configW.showIcons.setCheckState(Qt.Checked)
        else:
            self.configW.showIcons.setCheckState(Qt.Unchecked)
        self.configW.showIcons.stateChanged.connect(self.showIconsStateChanged)

        self.confirmDelete = int(self.settings.value("confirmDelete", int(Qt.Checked)))
        if self.confirmDelete == int(Qt.Checked):
            self.configW.confirmDelete.setCheckState(Qt.Checked)
        else:
            self.configW.confirmDelete.setCheckState(Qt.Unchecked)
        self.configW.confirmDelete.stateChanged.connect(self.confirmDeleteStateChanged)

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
        self.showThumbs = int(self.configW.showThumbs.checkState())
        self.settings.setValue("showThumbs", self.showThumbs)
        self.useInternalFileCopy = int(self.configW.useInternalFileCopy.checkState())
        self.settings.setValue("useInternalFileCopy", self.useInternalFileCopy)
        self.showIcons = int(self.configW.showIcons.checkState())
        self.settings.setValue("showIcons", self.showIcons)
        self.confirmDelete = int(self.configW.confirmDelete.checkState())
        self.settings.setValue("confirmDelete", self.confirmDelete)
                 
    def useCurrentLeft(self):
        self.configW.leftStartDir.setText(Df.d.lp.cd.path())

    def useCurrentRight(self):
        self.configW.rightStartDir.setText(Df.d.rp.cd.path())
        
    def showHiddenStateChanged(self, state):
        self.showHidden = int(state)

    def showThumbsStateChanged(self, state):
        self.showThumbs = int(state)

    def useInternalFileCopyStateChanged(self, state):
        self.useInternalFileCopy = int(state)

    def showIconsStateChanged(self, state):
        self.showIcons = int(state)

    def confirmDeleteStateChanged(self, state):
        self.confirmDelete = int(state)

    def licenseNag(self, title, text):    
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Information, title, text)
        msgBox.addButton("Try", QtGui.QMessageBox.AcceptRole)
        msgBox.addButton("Buy", QtGui.QMessageBox.RejectRole)
        msgBox.addButton("Enter key", QtGui.QMessageBox.ActionRole)
        r = msgBox.exec_()
        if r == 1:
            error = None
            try:
                if platform.system() == 'Windows':
                    os.startfile(genericPathToWindows("src/home.url"))
                else:
                    #os.chdir(self.parent.fspath)
                    subprocess.call(["xdg-open", "src/home.url"]) # TODO should run completely async
            except:
                t,error,tb = sys.exc_info()
            if error:
                error = str(error)
                print error
        elif r == 2:
            self.enterLicenseKey()

    def enterLicenseKey(self):
        lkey = Df_Dialog.Dialog("License", "Enter license key", "")
        if not lkey:
            return
        a = lkey.split(',')
        h = hashlib.sha1(a[0]+self.s).hexdigest()[0:8]
        if len(h) != 2 or h != a[1]:
            Df_Dialog.MessageWarn("License", "License key is invalid.")
        else:
            self.settings.setValue("lkey", lkey)
            Df.d.licenseKey = lkey
            
