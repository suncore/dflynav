
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
#sys.exit(0)

# Builder/main module

    
import sys
#, os
from PySide import QtCore, QtGui
import Df_Gui, Df_Dragonfly, Df_Panel, Df_StatusList, Df_ActionButtons, Df_Dialog
import Df, Df_Job, vfs, Df_GlobalButtons, Df_Mainwin, Df_Find
import platform, Df_Config, Df_Icon, Df_Preview, tempfile, os

if __name__ == '__main__':

    # d is the only global variable, the base object that contains the entier application state
    d = Df_Dragonfly.DragonFly()
    d.version = 1.0
    Df.d = d

    d.tempfile = tempfile.TemporaryFile()
    
    d.config = Df_Config.Config()
    
    d.fsNotify = [ None, None ]
    d.fsNotify[0] = vfs.Notify()
    d.fsNotify[1] = vfs.Notify()
    
    d.qtapp = QtGui.QApplication(sys.argv)
    d.iconFactory = Df_Icon.IconFactory()
    #d.qtapp.setStyle("plastique")
    #d.qtapp.setStyle("/a/dd/zz/qmc2-black-0.10/qmc2-black-0.10.qss")
    d.g = Df_Gui.Gui()
    d.g.mw = Df_Gui.MainWindow()
    #d.g.dia = Df_Gui.Dialog()
    d.g.config = Df_Gui.Config()
    d.g.jobstatus = Df_Gui.Jobstatus()
    d.g.help = Df_Gui.Help()
    d.g.find = Df_Gui.Find()
    #d.g.preview = Df_Gui.Preview()
    #d.g.mw.showMaximized()
    d.g.mw.setWindowIcon(QtGui.QIcon('src/icons/dragonfly.png'))
    d.g.mw.show()
    
    d.preview = Df_Preview.Preview(d.g.mw.left_preview_container, d.g.mw.right_preview_container, d.g.mw.left_preview_gv, d.g.mw.right_preview_gv, d.g.mw.left_preview_text, d.g.mw.right_preview_text, d.g.mw.left_tree, d.g.mw.right_tree)
    d.g.mw.right_preview_container.hide()
    d.g.mw.left_preview_container.hide()
    d.ab = Df_ActionButtons.ActionButtons(d.g.mw.actionButtonsLayout, d.g.mw.centralwidget)
    d.gb = Df_GlobalButtons.GlobalButtons(d.g.mw, d.g.config, d.g.help)
    
    d.history = []
    d.bookmarks = [ ]
    d.lp = Df_Panel.Panel(d.g.mw, d.g.mw.left_tree, d.g.mw.left_path, d.g.mw.left_status, d.g.mw.left_up, d.ab, 0, d.g.mw.toleft, d.g.mw.left_history, d.g.mw.left_bookmarks, d.g.mw.left_back, d.g.mw.left_find)
    d.rp = Df_Panel.Panel(d.g.mw, d.g.mw.right_tree, d.g.mw.right_path, d.g.mw.right_status, d.g.mw.right_up, d.ab, 1, d.g.mw.toright, d.g.mw.right_history, d.g.mw.right_bookmarks, d.g.mw.right_back, d.g.mw.right_find)
    d.lp.other = d.rp
    d.rp.other = d.lp
    #d.mainw = Df_Mainwin.Mainwin(d.g.mw, d.lp, d.rp)
    d.rp.start()
    d.lp.start()
    
    d.g.mw.left_up.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowUp))
    d.g.mw.right_up.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowUp))
    d.g.mw.toright.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowForward))
    d.g.mw.toleft.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowBack))
    #d.g.mw.help.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_DialogHelpButton))
    d.g.mw.left_back.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowBack))
    d.g.mw.right_back.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowBack))
    
    d.g.mw.splitter.setSizes([8000,1])
    d.g.mw.splitter.setStretchFactor(0,1)
    d.g.mw.splitter.setStretchFactor(1,0)
    
    d.g.mw.left_back.setToolTip("Back")
    d.g.mw.right_back.setToolTip("Back")
    d.g.mw.left_up.setToolTip("Up")
    d.g.mw.right_up.setToolTip("Up")
    d.g.mw.toleft.setToolTip("Set the left path to the same as the right path")
    d.g.mw.toright.setToolTip("Set the right path to the same as the left path")

    d.find = Df_Find.Find(d.g.find)    
    d.jobm = Df_Job.JobManager(d.g.mw.jobs, d.g.jobstatus)
    d.vfsJobm = vfs.vfs_asyncJobs.JobManager()
    
    def periodicTimer():
        Df.d.lp.periodicRefresh()
        Df.d.rp.periodicRefresh()
   
    d.timer = QtCore.QTimer()
    d.timer.timeout.connect(periodicTimer)
    d.timer.start(100)
    os.putenv('CYGWIN', 'nodosfilewarning')
    if platform.system() == 'Windows':
        path = os.getenv('PATH')
        if path[-1] != ";":
            path += ";"
        if os.path.exists("src/cygwin"):
            cwd = os.getcwd()
            path += cwd + "\\src\\cygwin\\bin" + ";" 
        else:
            path += "c:\\cygwin\\bin;"
        os.putenv('PATH', path)


    d.config.load(d.g.config)


    r = d.qtapp.exec_()
    d.fsNotify[0].stop()
    d.fsNotify[1].stop()
    d.config.save()
    d.tempfile.close()
    sys.exit(r)





#Extract icon from executable
#import sys
#import win32ui
#import win32gui
#from PySide import QtCore
#from PySide import QtGui
#
#class testWindow(QtGui.QMainWindow):
#    def __init__(self):
#        super(testWindow, self).__init__()
#        self.setGeometry(180.0, 130.0, 280.0, 400.0)
#        file = QtGui.QFileDialog.getOpenFileNames(self)
#        self.setMouseTracking(True)
#
#        large, small = win32gui.ExtractIconEx('C:/Program Files (x86)/Exact Audio Copy/eac.exe', 0)
#        win32gui.DestroyIcon(small[0])
#
#        self.pixmap = QtGui.QPixmap.fromWinHBITMAP(self.bitmapFromHIcon(large[0]), 2)
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
#        painter = QtGui.QPainter()
#        painter.begin(self)
#        painter.setRenderHint(QtGui.QPainter.Antialiasing)
#        painter.setPen(QtCore.Qt.NoPen)
#        painter.setBrush(QtGui.QBrush(QtGui.QColor(255.0, 255.0, 255.0, 255.0), QtCore.Qt.SolidPattern))
#        painter.drawRect(QtCore.QRect(0.0, 0.0, 280.0, 400.0))
#        painter.drawPixmap(QtCore.QRect(0.0, 0.0, 32.0, 32.0), self.pixmap)
#        painter.end()
#
#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
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
