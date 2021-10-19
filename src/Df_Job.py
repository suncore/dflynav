import os, stat, time
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
import _thread
from utils import *
from queue import Queue


class Cmd(object):
    def __init__(self, args):
        pass

    def readline(self):
        pass
    
    def finish(self):
        pass

class JobManager(object):
    def __init__(self, jobsW, jobstatusW):
        self.jobsW = jobsW
        self.jobstatusW = jobstatusW
        self.q = Queue()
        self.jobs = []
        self.jobIndex = 0
        self.jobsW.setColumnCount(0)
        self.jobsW.setHeaderLabels( [ "Time", "Command", "Status" ] )
        self.jobsW.header().setStretchLastSection(False)
        self.jobsW.header().hide()
        self.jobsW.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.jobsW.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.jobsW.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.jobsW.itemPressed.connect(self.mouseButtonPressed)
        self.jobstatusW.close.clicked.connect(self.closeClicked)
        self.jobstatusW.stop.clicked.connect(self.stopClicked)
        self.jobStatusWindowActive = False
        self.runningJob = None
        self.jobStatusWindowJob = None
        self.jobstatusW.start.hide() # Can't start jobs prematurely yet
        _thread.start_new_thread(self.jobTask, (self,))

    def closeClicked(self):
        self.jobStatusWindowActive = False
        self.jobstatusW.hide()
        self.jobsW.clearSelection()

    def stopClicked(self):
        self.jobStatusWindowJob.processed = True
        self.jobStatusWindowJob.setStatus("Aborted")
        if self.runningJob == self.jobStatusWindowJob:
            self.runningJob.runCmd.stop()

    def addJob(self, executer, args, cmd, showStatusNow=False, ignoreError=False):
        job = Job(args, executer, cmd, self, ignoreError)
        job.setStatus("Queued")
        self.jobs.append(job)
        self.q.put(1)
        if showStatusNow:
            self.showJobStatusWindow(job)

    def addJobDone(self, cmd, error):
        job = JobDone(cmd, error, self)
        if error:
            job.setStatus("Failed")
        else:
            job.setStatus("Done")

    def jobTask(self, dummy):
        try:
            while True:
                x = self.q.get(True)
                while self.jobIndex < len(self.jobs):
                    job = self.jobs[self.jobIndex]
                    if job.processed:
                        self.jobIndex += 1
                        continue
                    job.processed = True
                    job.setStatus("Running")
    
                    job.runCmd = job.executer(job.args)
                    if job.runCmd.error:
                        job.output += job.runCmd.error
                        job.setStatus("Failed")
                    else:
                        self.runningJob = job
                        output = job.runCmd.readline()
                        while output:
                            job.output += output
                            job.setStatus()
                            output = job.runCmd.readline()
                        status = job.runCmd.finish()
                        self.runningJob = None
                        job.output = job.output.rstrip()
                        if status != 0 and not job.ignoreError:
                            job.setStatus("Failed")
                        else:
                            job.setStatus("Done")
                    self.jobIndex += 1
        except:
            crash()

    def mouseButtonPressed(self, item):
        self.showJobStatusWindow(item.df_entry)

    def showJobStatusWindow(self, job):
        self.jobStatusWindowActive = True
        self.jobStatusWindowJob = job
        self.jobStatusWindowJob.setStatus()
        self.jobstatusW.show()

class Communicate(QObject):
    setStatus = pyqtSignal()

class Entry(object):
    def __init__(self, cmd, jobManager):
        item = QtWidgets.QTreeWidgetItem( [ '', cmd, "" ] )
        self.jobManager = jobManager
        self.jobManager.jobsW.insertTopLevelItem(0, item)
        self.item = item
        item.df_entry = self
        self.cmd = cmd
        self.statusString = ""
        self.output = ''
        self.c = Communicate()
        self.c.setStatus.connect(self.setStatus2)

    def setStatus(self, string = ""):
        if string != "":    
            self.statusString = string
        self.c.setStatus.emit()

    def setStatus2(self):
        # This runs in the GUI thread
        self.item.setText(0, time2str(timenow()))
        self.item.setText(2, self.statusString)
        if self.statusString == "Failed":
            self.item.setBackground(2, QtGui.QColor('#700000'))
            self.item.setForeground(2, Qt.white)
        elif self.statusString == "Done":
            self.item.setBackground(2, QtGui.QColor('#005000'))
            self.item.setForeground(2, Qt.white)
        elif self.statusString == "Running":
            self.item.setBackground(2, QtGui.QColor('#505000'))
            self.item.setForeground(2, Qt.white)


        if self.jobManager.jobStatusWindowActive and self == self.jobManager.jobStatusWindowJob:
            jsw = self.jobManager.jobstatusW
            jsw.output.clear()
            out = self.output
            if out == "" and self.statusString == "Done":
                out = "OK"
            try:
                cmd = "\n\nCommand:\n" + self.args[1] + " $ " + ' '.join(self.args[0]) # self.args does not always exist
            except:
                cmd = ""
            jsw.output.insertPlainText(self.cmd + "\n\nResult: \n" + out + cmd)
            jsw.status.setText("Status: "+self.statusString)
            eq = self.statusString == "Queued"
            er = self.statusString == "Running"
            jsw.start.setEnabled(eq)
            jsw.stop.setEnabled(er or eq)

        

class Job(Entry):
    def __init__(self, args, executer, cmd, jobsW, ignoreError):
        super(Job, self).__init__(cmd, jobsW)
        self.args = args
        self.executer = executer
        self.processed = False
        self.runCmd = None
        self.ignoreError = ignoreError

class JobDone(Entry):
    def __init__(self, cmd, error, jobsW):
        super(JobDone, self).__init__(cmd, jobsW)
        if error:
            self.output = error

