
# Builder/main module

    
import sys
#, os
from PySide import QtCore, QtGui
import Df_Gui, Df_Dragonfly, Df_Panel, Df_StatusList, Df_ActionButtons, Df_Dialog
import Df, Df_Job, vfs
import platform, Df_Config, Df_Icon

def refresh():
    d.lp.setPath(d.lp.cd)
    d.rp.setPath(d.rp.cd)

if __name__ == '__main__':

    # d is the only global variable, the base object that contains the entier application state
    d = Df_Dragonfly.DragonFly()
    Df.d = d
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
    d.g.dia = Df_Gui.Dialog()
    #d.g.mw.showMaximized()
    d.g.mw.show()
    
    d.ab = Df_ActionButtons.ActionButtons(d.g.mw.actionButtonsLayout, d.g.mw.centralwidget)
    
    d.history = []
    d.bookmarks = [ ]
    d.lp = Df_Panel.Panel(d.g.mw, d.g.mw.left_tree, d.g.mw.left_path, d.g.mw.left_status, d.g.mw.left_up, d.ab, 0, d.g.mw.toleft, d.g.mw.left_history, d.g.mw.left_bookmarks, d.g.mw.left_back)
    d.rp = Df_Panel.Panel(d.g.mw, d.g.mw.right_tree, d.g.mw.right_path, d.g.mw.right_status, d.g.mw.right_up, d.ab, 1, d.g.mw.toright, d.g.mw.right_history, d.g.mw.right_bookmarks, d.g.mw.right_back)
    d.lp.other = d.rp
    d.rp.other = d.lp
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
    
    d.jobm = Df_Job.JobManager(d.g.mw.jobs)
    d.vfsJobm = vfs.vfs_asyncJobs.JobManager()
    
    def periodicTimer():
        Df.d.lp.periodicRefresh()
        Df.d.rp.periodicRefresh()
   
    d.timer = QtCore.QTimer()
    d.timer.timeout.connect(periodicTimer)
    d.timer.start(100)
    #os.putenv('nodosfilewarning','1')
    
    d.g.mw.refresh.clicked.connect(refresh)

    d.config.Load()

    r = d.qtapp.exec_()
    d.fsNotify[0].stop()
    d.fsNotify[1].stop()
    d.config.Save()
    sys.exit(r)





#
#import sys
#from PySide import QtCore, QtGui
#
#class MainForm(QtGui.QMainWindow):
#    def __init__(self, parent=None):
#        super(MainForm, self).__init__(parent)
#
#        # create button
#        #self.button = QtGui.QPushButton("test button", self)       
#        self.button = QtGui.QLabel("test button", self)       
#        self.button.resize(100, 30)
#
#        # set button context menu policy
#        self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#        self.button.customContextMenuRequested.connect(self.on_context_menu)
#
#        #self.connect(self.button, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
#
#        # create context menu
#        self.popMenu = QtGui.QMenu(self)
#        self.popMenu.addAction(QtGui.QAction('test0', self))
#        self.popMenu.addAction(QtGui.QAction('test1', self))
#        self.popMenu.addSeparator()
#        self.popMenu.addAction(QtGui.QAction('test2', self))        
#
#    def on_context_menu(self, point):
#        # show context menu
#        self.popMenu.exec_(self.button.mapToGlobal(point))        
#
#def main():
#    app = QtGui.QApplication(sys.argv)
#    form = MainForm()
#    form.show()
#    app.exec_()
#
#if __name__ == '__main__':
#    main()
#    
    

#
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
