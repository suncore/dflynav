import os, stat, time
from PySide.QtCore import *
from PySide import QtGui
import thread
from utils import *
from Queue import Queue


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
        self.jobsW.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.jobsW.header().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.jobsW.header().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        thread.start_new_thread(self.jobTask, (self,))
        self.jobsW.itemPressed.connect(self.mouseButtonPressed)
        self.jobstatusW.close.clicked.connect(self.closeClicked)
        self.jobstatusW.stop.clicked.connect(self.stopClicked)
        self.jobStatusWindowActive = False
        self.runningJob = None
        self.jobStatusWindowJob = None
        #self.jobstatusW.command.hide()
        self.jobstatusW.start.hide()

    def closeClicked(self):
        self.jobStatusWindowActive = False
        self.jobstatusW.hide()

    def stopClicked(self):
        self.jobStatusWindowJob.processed = True
        self.jobStatusWindowJob.setStatus("Aborted")
        if self.runningJob:
            self.runningJob.runCmd.stop()

    def addJob(self, executer, args, cmd):
        job = Job(args, executer, cmd, self.jobsW)
        job.setStatus("Queued")
        self.jobs.append(job)
        job.updateTime()
        self.q.put(1)

    def addJobDone(self, cmd, error):
        job = JobDone(cmd, error, self.jobsW)
        job.updateTime()
        if error:
            job.setStatus("Failed")
            #job.setToolTip(error)
        else:
            job.setStatus("Done")

    def jobTask(self, dummy):
        try:
            while True:
                x = self.q.get(True)
                while self.jobIndex < len(self.jobs):
                    #a = crashme()
                    job = self.jobs[self.jobIndex]
                    if job.processed:
                        continue
                    job.processed = True
                    job.updateTime()
                    job.setStatus("Running")
                    self.updateJobStatusWindow(job)
    
                    job.runCmd = job.executer(job.args)
                    if job.runCmd.error:
                        job.output += job.runCmd.error
                        job.setStatus("Failed")
                    else:
                        self.runningJob = job
                        output = job.runCmd.readline()
                        #print output
                        while output:
                            job.output += output
                            self.updateJobStatusWindow(job)
                            output = job.runCmd.readline()
                            #print output
                        status = job.runCmd.finish()
                        self.runningJob = None
                        job.output = job.output.rstrip()
                        #print job.output
                        if status != 0:
                            job.setStatus("Failed")
                        else:
                            job.setStatus("Done")
                    #job.setToolTip(job.output)
                    job.updateTime()
                    self.updateJobStatusWindow(job)
                    self.jobIndex += 1
        except:
            crash()

    def mouseButtonPressed(self, item):
        self.jobStatusWindowActive = True
        self.jobstatusW.output.clear()
        out = n.output
        if out == "" and n.statusString == "Done":
            out = "OK"
        self.jobstatusW.output.insertPlainText("Command:\n" + n.cmd + "\n\nOutput from command: \n" + out)
        self.updateJobStatusWindow(item.df_entry)
        self.jobstatusW.show()
        
    def updateJobStatusWindow(self, n):
        if self.jobStatusWindowActive:
            self.jobStatusWindowJob = n
            self.jobstatusW.output.insertPlainText(n.output)
            self.jobstatusW.status.setText("Status: "+n.statusString)
            eq = n.statusString == "Queued"
            er = n.statusString == "Running"
            self.jobstatusW.start.setEnabled(eq)
            self.jobstatusW.stop.setEnabled(er or eq)
        

class Entry(object):
    def __init__(self, cmd, jobsW):
        item = QtGui.QTreeWidgetItem( [ '', cmd, "" ] )
        jobsW.insertTopLevelItem(0, item)
        self.item = item
        item.df_entry = self
        self.cmd = cmd
        self.statusString = ""
        self.output = ''

    def setStatus(self, string):
        self.statusString = string
        self.item.setText(2, string)
        if string == "Failed":
            self.item.setBackground(2, Qt.red)
            self.item.setForeground(2, Qt.white)
#        elif string == "Running":
#            self.item.setBackground(2, Qt.green)
#            self.item.setForeground(2, Qt.white)
        
    def updateTime(self):
        self.item.setText(0, time2str(timenow()))

#    def setToolTip(self, msg):
#        return
#        for i in range(0,3):
#            self.item.setToolTip(i, msg)

class Job(Entry):
    def __init__(self, args, executer, cmd, jobsW):
        super(Job, self).__init__(cmd, jobsW)
        self.args = args
        self.executer = executer
        self.processed = False
        self.runCmd = None

class JobDone(Entry):
    def __init__(self, cmd, error, jobsW):
        super(JobDone, self).__init__(cmd, jobsW)
        if error:
            self.output = error

