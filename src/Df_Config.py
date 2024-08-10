from PyQt6.QtCore import *
from PyQt6 import QtGui
from utils import *
import Df, time, hashlib, sys, Df_Dialog, os, locale

def checkstate2int(cs):
    if cs == Qt.CheckState.Checked:
        return 1
    return 0

class Config():
    def __init__(self):
        self.settings = QSettings("Dragonfly", "Dragonfly Navigator")
        locale.setlocale(locale.LC_TIME, '')
        self.formatTimeDate = '%x %X'
    
    def load(self, configW):
        self.configW = configW
        Df.d.startCount = int(self.settings.value("startCount", 0))+1

        pos = self.settings.value("pos", QPoint(100, 100))
        size = self.settings.value("size", QSize(1024, 768))
        maximized = self.settings.value("maximized", 1)
        if maximized == 1:
            Df.d.g.mw.setWindowState(Qt.WindowState.WindowMaximized)
        else:
            Df.d.g.mw.resize(size)
        Df.d.g.mw.move(pos)

        Df.d.bookmarks = self.settings.value("bookmarks", [ "None" ])
        if Df.d.bookmarks == [ "None" ]:
            Df.d.bookmarks = [ ]
        Df.d.lp.updateBookmarksMenu()
        Df.d.rp.updateBookmarksMenu()

        Df.d.history = self.settings.value("history", [ "None" ])
        if Df.d.history == [ "None" ]:
            Df.d.history = [ ]
        Df.d.lp.updateHistoryMenu()
        Df.d.rp.updateHistoryMenu()

        self.rememberStartDirs = bool(int(self.settings.value("rememberStartDirs", 1)))
        if self.rememberStartDirs:
            self.configW.rememberStartFolders.setChecked(True)
            self.configW.startAtSpecifiedFolders.setChecked(False)
        else:
            self.configW.rememberStartFolders.setChecked(False)
            self.configW.startAtSpecifiedFolders.setChecked(True)

        self.showHidden = int(self.settings.value("showHidden", checkstate2int(Qt.CheckState.Unchecked)))
        if self.showHidden == checkstate2int(Qt.CheckState.Checked):
            self.configW.showHidden.setCheckState(Qt.CheckState.Checked)
        else:
            self.configW.showHidden.setCheckState(Qt.CheckState.Unchecked)

        self.showThumbs = int(self.settings.value("showThumbs", checkstate2int(Qt.CheckState.Checked)))
        if self.showThumbs == checkstate2int(Qt.CheckState.Checked):
            self.configW.showThumbs.setCheckState(Qt.CheckState.Checked)
        else:
            self.configW.showThumbs.setCheckState(Qt.CheckState.Unchecked)

        self.confirmDelete = int(self.settings.value("confirmDelete", checkstate2int(Qt.CheckState.Checked)))
        if self.confirmDelete == checkstate2int(Qt.CheckState.Checked):
            self.configW.confirmDelete.setCheckState(Qt.CheckState.Checked)
        else:
            self.configW.confirmDelete.setCheckState(Qt.CheckState.Unchecked)

        self.configW.useCurrentLeft.clicked.connect(self.useCurrentLeft)
        self.configW.useCurrentRight.clicked.connect(self.useCurrentRight)
        self.configW.buttonBox.accepted.connect(self.accepted)
        
        #self.configW.rememberStartFolders.clicked.connect(self.rememberStartFoldersClicked)
        #self.configW.startAtSpecifiedFolders.clicked.connect(self.startAtSpecifiedFoldersClicked)

        homedir = os.getenv('HOME')
        self.startDirLeft = self.settings.value("startDirLeft",homedir)        
        self.startDirRight = self.settings.value("startDirRight",homedir)        
        self.configW.leftStartDir.setText(self.startDirLeft)
        self.configW.rightStartDir.setText(self.startDirRight)
        self.save()
        Df.d.lp.setPathByString(self.startDirLeft)
        Df.d.rp.setPathByString(self.startDirRight)
        self.save()

    def accepted(self):
        self.save()
        Df.d.lp.refresh()
        Df.d.rp.refresh()
        
    def save(self):
        self.settings.setValue("pos", Df.d.g.mw.pos())
        self.settings.setValue("size", Df.d.g.mw.size())
        self.settings.setValue("startCount", Df.d.startCount)
        state = Df.d.g.mw.windowState()
        maximized = Df.d.g.mw.windowState() == Qt.WindowState.WindowMaximized
        self.settings.setValue("maximized", int(maximized))
        if Df.d.bookmarks == []:
            self.settings.setValue("bookmarks", [ "None" ])
        else:
            self.settings.setValue("bookmarks", Df.d.bookmarks)
        if Df.d.history == []:
            self.settings.setValue("history", [ "None" ])
        else:
            self.settings.setValue("history", Df.d.history)
        self.rememberStartDirs = self.configW.rememberStartFolders.isChecked()
        self.settings.setValue("rememberStartDirs", int(self.rememberStartDirs))
        if self.rememberStartDirs:
            self.settings.setValue("startDirLeft", Df.d.lp.cd.path())
            self.settings.setValue("startDirRight", Df.d.rp.cd.path())
            #print(Df.d.lp.cd.path(), Df.d.rp.cd.path())
        else:
            self.settings.setValue("startDirLeft", self.configW.leftStartDir.text())
            self.settings.setValue("startDirRight", self.configW.rightStartDir.text())

        self.showHidden = checkstate2int(self.configW.showHidden.checkState())
        self.settings.setValue("showHidden", self.showHidden)
        self.showThumbs = checkstate2int(self.configW.showThumbs.checkState())
        self.settings.setValue("showThumbs", self.showThumbs)
        self.confirmDelete = checkstate2int(self.configW.confirmDelete.checkState())
        self.settings.setValue("confirmDelete", self.confirmDelete)
        
        self.settings.sync()
                 
    def useCurrentLeft(self):
        self.configW.leftStartDir.setText(Df.d.lp.cd.path())

    def useCurrentRight(self):
        self.configW.rightStartDir.setText(Df.d.rp.cd.path())
        
#    def licenseNag(self, title, text):    
#        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, title, text)
#        msgBox.addButton("Try", QtWidgets.QMessageBox.AcceptRole)
#        msgBox.addButton("Buy", QtWidgets.QMessageBox.RejectRole)
#        msgBox.addButton("Enter key", QtWidgets.QMessageBox.ActionRole)
#        r = msgBox.exec_()
#        if r == 1:
#            error = None
#            try:
#                if platform.system() == 'Windows':
#                    os.startfile(genericPathToWindows("src/home.url"))
#                else:
#                    #os.chdir(self.parent.fspath)
#                    subprocess.call(["xdg-open", "src/home.url"]) # TODO should run completely async
#            except:
#                t,error,tb = sys.exc_info()
#            if error:
#                error = str(error)
#                print error
#        elif r == 2:
#            self.enterLicenseKey()
#
#    def licenseCheck(self, lkey):
#        try:
#            a = lkey.split(',')
#            h = hashlib.sha1(a[0]+a[1]+self.s).hexdigest()[0:8]
#            if h == a[2]:
#                return True
#        except:
#            pass
#        return False
#
#    def enterLicenseKey(self):
#        lkey = Df_Dialog.Dialog("License", "Enter license key", "")
#        r = self.licenseCheck(lkey)
#        if r:
#            self.settings.setValue("lkey", lkey)
#            Df.d.licenseKey = lkey
#        else:
#            Df_Dialog.MessageWarn("License", "License key is invalid.")
            
