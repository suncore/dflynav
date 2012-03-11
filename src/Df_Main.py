# Builder/main module

import sys
#, os
from PySide import QtCore, QtGui
import Df_Gui, Df_Dragonfly, Df_Panel, Df_StatusList, Df_ActionButtons
import Df, Df_Job, vfs

if __name__ == '__main__':

    # d is the only global variable, the base object that contains the entier application state
    d = Df_Dragonfly.DragonFly()
    
    d.fsNotify = [ None, None ]
    d.fsNotify[0] = vfs.Notify()
    d.fsNotify[1] = vfs.Notify()
    
    d.qtapp = QtGui.QApplication(sys.argv)
    #d.qtapp.setStyle("plastique")
    #d.qtapp.setStyle("/a/dd/zz/qmc2-black-0.10/qmc2-black-0.10.qss")
    d.g = Df_Gui.Gui()
    d.g.mw = Df_Gui.MainWindow()
    d.g.dia = Df_Gui.Dialog()
    #d.g.mw.showMaximized()
    d.g.mw.show()
    #d.g.dia.show()
    
    d.ab = Df_ActionButtons.ActionButtons(d.g.mw.actionButtonsLayout, d.g.mw.centralwidget)
    
    d.lp = Df_Panel.Panel(d.g.mw.left_tree, d.g.mw.left_path, d.g.mw.left_status, d.g.mw.left_up, d.ab, 0)
    d.rp = Df_Panel.Panel(d.g.mw.right_tree, d.g.mw.right_path, d.g.mw.right_status, d.g.mw.right_up, d.ab, 1)
    d.lp.other = d.rp
    d.rp.other = d.lp
    d.rp.start()
    d.lp.start()
    
    #d.sl = Df_StatusList.StatusList(d.g.mw.statusbar)
    #d.sl.setText('Welcome to Dragonfly Navigator 1.0')
    
    d.g.mw.left_up.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowUp))
    d.g.mw.right_up.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowUp))
    d.g.mw.toright.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowForward))
    d.g.mw.toleft.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_ArrowBack))
    #d.g.mw.help.setIcon(d.g.mw.style().standardIcon(QtGui.QStyle.SP_DialogHelpButton))
    
    d.g.mw.splitter.setSizes([8000,1])
    d.g.mw.splitter.setStretchFactor(0,1)
    d.g.mw.splitter.setStretchFactor(1,0)
    
    d.jobm = Df_Job.JobManager(d.g.mw.jobs)
    
    Df.d = d
    
    d.lp.setPathByString("/Files/Local/a/proj/dragonfly/src/test")
    d.rp.setPathByString("/Files/Local/a/proj/dragonfly/src/test")
    
    def oneSecTimer():
        Df.d.lp.periodicRefresh()
        Df.d.rp.periodicRefresh()
   
    d.timer = QtCore.QTimer()
    d.timer.timeout.connect(oneSecTimer)
    d.timer.start(1000)
    #os.putenv('nodosfilewarning','1')
    r = d.qtapp.exec_()
    d.fsNotify[0].stop()
    d.fsNotify[1].stop()
    sys.exit(r)
