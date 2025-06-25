#!/usr/bin/env python3
#import win32con, sys
#from win32com.shell import shell, shellcon
#
#flags = shellcon.SHGFI_LARGEICON | shellcon.SHGFI_ICON | \
#        shellcon.SHGFI_USEFILEATTRIBUTES
#hr, info = shell.SHGetFileInfo('pdf', win32con.FILE_ATTRIBUTE_NORMAL,
#                               flags)
#hicon, iicon, attr, display_name, type_name = info
#print info
#
#from utils import *
#print WindowsGetIconFilenameFromExt('pdf')
#print WindowsGetIconFilenameFromExt('gif')
#sys.exit(0)

# Builder/main module
#import time
#print(time.strftime("%x %X",time.localtime(time.time())))

#import setproctitle
#setproctitle.setthreadtitle('dragonfly')
#setproctitle.setproctitle('dragonfly')
    
import sys
#print(sys.argv[0])
sys.path.insert(0, "3pp")
#, os
from PyQt6 import QtCore, QtGui, QtWidgets
import Df_Gui, Df_Dragonfly, Df_Panel, Df_StatusList, Df_ActionButtons, Df_Dialog
import Df, Df_Job, vfs, Df_GlobalButtons, Df_Mainwin, Df_Find
import platform, Df_Config, Df_Icon, Df_Preview, tempfile, os
import sys, traceback, Df_Bugreport
from utils import *
from queue import Queue
import _thread
from PIL import Image
from pillow_heif import register_heif_opener

#from cykooz.heif.pil import register_heif_opener

# sys.path = [
#     '/usr/lib/python39.zip',
#     '/usr/lib/python3.9',
#     '/usr/lib/python3.9/lib-dynload',
#     '/usr/lib/python3/dist-packages',
# ]


def main():

#if __name__=="__main__":

    register_heif_opener()

    iconFile = 'icons/dragonfly.png'

    # d is the only global variable, the base object that contains the entire application state
    d = Df_Dragonfly.DragonFly()
    d.version = "21.0"
    d.appdata = None
    d.previousLog = ""
    d.logfile = None

    try:
        d.appdata = os.getenv('HOME') + '/.config/Dragonfly'
        if not os.path.exists(d.appdata):
            os.mkdir(d.appdata)
        d.logfile = os.path.join(d.appdata, "dragonfly_navigator.log")
        if os.path.exists(d.logfile):
            f = open(d.logfile, "r")
            d.previousLog = f.read()
            f.close()
            #os.remove(d.logfile)
        f = open(d.logfile, 'w') 
        f.close()
#        sys.stdout = f
#        sys.stderr = f
#        f = None
    except:
        pass
            
    Df.d = d

    d.tempfile = tempfile.TemporaryFile()
    d.uidgrpCache = {}
    d.config = Df_Config.Config()
    
    d.fsNotify = [ None, None ]
    d.fsNotify[0] = vfs.Notify()
    d.fsNotify[1] = vfs.Notify()

    d.qtapp = QtWidgets.QApplication(sys.argv)
    d.qtapp.setDesktopFileName("dragonfly")
    d.g = Df_Gui.Gui()
    d.g.mw = Df_Gui.MainWindow()
    d.iconFactory = Df_Icon.IconFactory(d.g.mw.help.height())
    d.g.config = Df_Gui.Config()
    d.g.config.setWindowIcon(QtGui.QIcon(iconFile))
    d.g.jobstatus = Df_Gui.Jobstatus()
    d.g.jobstatus.setWindowIcon(QtGui.QIcon(iconFile))
    d.g.help = Df_Gui.Help()
    d.g.help.setWindowIcon(QtGui.QIcon(iconFile))
    d.g.find = Df_Gui.Find()
    d.g.find.setWindowIcon(QtGui.QIcon(iconFile))
    #d.g.mw.showMaximized()
    d.g.mw.setWindowIcon(QtGui.QIcon(iconFile))
    d.g.mw.show()
    
    d.preview = Df_Preview.Preview(d.g.mw.left_preview_container, d.g.mw.right_preview_container, d.g.mw.left_preview_gv, d.g.mw.right_preview_gv, d.g.mw.left_preview_text, d.g.mw.right_preview_text, d.g.mw.left_tree, d.g.mw.right_tree, d.g.mw.left_text, d.g.mw.right_text)
    d.g.mw.right_preview_container.hide()
    d.g.mw.left_preview_container.hide()
    d.g.mw.right_text.hide()
    d.g.mw.left_text.hide()
    d.ab = Df_ActionButtons.ActionButtons(d.g.mw.actionButtonsLayout, d.g.mw.centralwidget)
    d.gb = Df_GlobalButtons.GlobalButtons(d.g.mw, d.g.config, d.g.help)
    
    d.history = []
    d.bookmarks = [ ]
    d.panelIconQueue = Queue()
    _thread.start_new_thread(Df_Panel.PanelIconQueueTask,("",))
    d.lp = Df_Panel.Panel(d.g.mw, d.g.mw.left_tree, d.g.mw.left_path, d.g.mw.left_status, d.g.mw.left_up, d.ab, 0, d.g.mw.toleft, d.g.mw.left_history, d.g.mw.left_bookmarks, d.g.mw.left_back, d.g.mw.left_find, d.g.mw.left_terminal, d.g.mw.left_reload, d.g.mw.left_mkdir, d.g.mw.right_text)
    d.rp = Df_Panel.Panel(d.g.mw, d.g.mw.right_tree, d.g.mw.right_path, d.g.mw.right_status, d.g.mw.right_up, d.ab, 1, d.g.mw.toright, d.g.mw.right_history, d.g.mw.right_bookmarks, d.g.mw.right_back, d.g.mw.right_find, d.g.mw.right_terminal, d.g.mw.right_reload, d.g.mw.right_mkdir, d.g.mw.left_text)
    d.lp.other = d.rp
    d.rp.other = d.lp
    #d.mainw = Df_Mainwin.Mainwin(d.g.mw, d.lp, d.rp)
    class Refresh(QObject):
        refreshSig = pyqtSignal()
    
    def periodicTimer():
        Df.d.lp.periodicRefresh()
        Df.d.rp.periodicRefresh()

    d.refresh = Refresh()
    d.refresh.refreshSig.connect(periodicTimer)
   
#    d.timer = QtCore.QTimer()
#    d.timer.timeout.connect(periodicTimer)
#    d.timer.start(100)


    d.find = Df_Find.Find(d.g.find)    
    d.jobm = Df_Job.JobManager(d.g.mw.jobs, d.g.jobstatus)
    d.vfsJobm = vfs.vfs_asyncJobs.JobManager()

    d.config.load(d.g.config)
    #print(sys.argv, sys.argv[-2], sys.argv[-1])
    if sys.argv[-2] != "":
        Df.d.lp.setPathByString(sys.argv[-2])
    if sys.argv[-1] != "":
        Df.d.rp.setPathByString(sys.argv[-1])
    d.rp.start()
    d.lp.start()
    style = d.g.mw.style()
    d.g.mw.left_up.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowUp))
    d.g.mw.right_up.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowUp))
    d.g.mw.toright.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowForward))
    d.g.mw.toleft.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowBack))
    #d.g.mw.help.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DialogHelpButton))
    d.g.mw.left_back.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowBack))
    d.g.mw.right_back.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowBack))
    d.g.mw.left_reload.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_BrowserReload))
    d.g.mw.right_reload.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_BrowserReload))
    d.g.mw.left_terminal.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ComputerIcon))
    d.g.mw.right_terminal.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ComputerIcon))
    d.g.mw.left_find.setIcon(QtGui.QIcon.fromTheme("search"))
    d.g.mw.right_find.setIcon(QtGui.QIcon.fromTheme("search"))

    d.g.mw.splitter.setSizes([8000,1])
    d.g.mw.splitter.setStretchFactor(0,1)
    d.g.mw.splitter.setStretchFactor(1,0)
    
    d.g.mw.left_back.setToolTip("Go to previous directory")
    d.g.mw.right_back.setToolTip("Go to previous directory")
    d.g.mw.left_up.setToolTip("Go to parent directory")
    d.g.mw.right_up.setToolTip("Go to parent directory")
    d.g.mw.toleft.setToolTip("Set the left path to the same as the right path")
    d.g.mw.toright.setToolTip("Set the right path to the same as the left path")
    d.g.mw.left_reload.setToolTip("Reload")
    d.g.mw.right_reload.setToolTip("Reload")
    d.g.mw.left_terminal.setToolTip("Terminal")
    d.g.mw.right_terminal.setToolTip("Terminal")
    d.g.mw.left_find.setToolTip("Search...")
    d.g.mw.right_find.setToolTip("Search...")
    
    Df_Bugreport.CheckForCrashReport()
    if d.startCount == 1:
        d.gb.help()
    r = d.qtapp.exec()
    d.fsNotify[0].stop()
    d.fsNotify[1].stop()
    d.config.save()
    d.tempfile.close()
    #sys.exit(r)


if __name__=="__main__":
    
    #print("Hello world")
    #print("\n")
    sys.stdout.flush()
    #main()
    #sys.exit(0)
    #print("Hello", file=sys.stderr)
    if os.environ.get("RELEASE") == "True":
        #print("Release")
        try:
            main()
        except:
            #traceback.print_exc()
            crash()
            #raise
    else:
        #print("Debug")
        #print("\n")
        main()
    #sys.exit(0)





#Extract icon from executable
#import sys
#import win32ui
#import win32gui
#from PyQt6 import QtCore
#from PyQt6 import QtGui
#
#class testWindow(QtWidgets.QMainWindow):
#    def __init__(self):
#        super(testWindow, self).__init__()
#        self.setGeometry(180.0, 130.0, 280.0, 400.0)
#        file = QtWidgets.QFileDialog.getOpenFileNames(self)
#        self.setMouseTracking(True)
#
#        large, small = win32gui.ExtractIconEx('C:/Program Files (x86)/Exact Audio Copy/eac.exe', 0)
#        win32gui.DestroyIcon(small[0])
#
#        self.pixmap = QtWidgets.QPixmap.fromWinHBITMAP(self.bitmapFromHIcon(large[0]), 2)
#    def bitmapFromHIcon(self, hIcon):
#        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
#        hbmp = win32ui.CreateBitmap()
#        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
#        hdc = hdc.CreateCompatibleDC()
#        hdc.SelectObject(hbmp)
#        hdc.DrawIcon((0, 0), hIcon)
#        hdc.DeleteDC()
#        return hbmp.GetHandle()
#    def paintEvent(self, event):
#        painter = QtWidgets.QPainter()
#        painter.begin(self)
#        painter.setRenderHint(QtWidgets.QPainter.Antialiasing)
#        painter.setPen(QtCore.Qt.NoPen)
#        painter.setBrush(QtWidgets.QBrush(QtWidgets.QColor(255.0, 255.0, 255.0, 255.0), QtCore.Qt.SolidPattern))
#        painter.drawRect(QtCore.QRect(0.0, 0.0, 280.0, 400.0))
#        painter.drawPixmap(QtCore.QRect(0.0, 0.0, 32.0, 32.0), self.pixmap)
#        painter.end()
#
#if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    mainWindow = testWindow()
#    mainWindow.show()
#    app.exec_()
#    
#sys.exit(0)


#import win32ui
#import win32gui
#import win32con
#import win32api
#import cStringIO
#import Image
#
#tempDirectory = os.getenv("temp")
#ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
#
#dst = cStringIO.StringIO()
#
#large, small = win32gui.ExtractIconEx(path,0)
#win32gui.DestroyIcon(small[0])
#       
##creating a destination memory DC
#hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
#hbmp = win32ui.CreateBitmap()
#hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
#hdc = hdc.CreateCompatibleDC()
#       
#hdc.SelectObject( hbmp )
#       
##draw a icon in it
#hdc.DrawIcon( (0,0), large[0] )
#win32gui.DestroyIcon(large[0])
#
##convert picture
#hbmp.SaveBitmapFile( hdc, tempDirectory + "\Icontemp.bmp")
#
#im = Image.open(tempDirectory + "\Icontemp.bmp")
#im.save(dst, "JPEG")
#
#dst.seek(0)
#
#os.remove(tempDirectory + "\Icontemp.bmp")    
#return dst.read()


#Browsing windows network shares:
#def test():
#    import win32com.client 
#    strComputer = "server" 
#    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
#    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
#    colItems = objSWbemServices.ExecQuery("Select * from Win32_Share") 
#    for objItem in colItems: 
#        print "Access Mask: ", objItem.AccessMask 
#        print "Allow Maximum: ", objItem.AllowMaximum 
#        print "Caption: ", objItem.Caption 
#        print "Description: ", objItem.Description 
#        print "Install Date: ", objItem.InstallDate 
#        print "Maximum Allowed: ", objItem.MaximumAllowed 
#        print "Name: ", objItem.Name 
#        print "Path: ", objItem.Path 
#        print "Status: ", objItem.Status 
#        print "Type: ", objItem.Type 
