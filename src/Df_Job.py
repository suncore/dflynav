import os, stat, time
from PySide.QtCore import *
from PySide import QtGui
import thread
from utils import *

class JobManager():
    def __init__(self, jobsW):
        self.jobsW = jobsW
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
    
    def addJobs(self, fun, srcList, dst):
        for src in srcList:
            job = Job(fun, src, dst)
            self.jobs.append(job)
            job.item = QtGui.QTreeWidgetItem( [ '', job.cmdString, "Queued" ] )
            job.updateTime()
            self.jobsW.insertTopLevelItem(0, job.item)

    def jobTask(self, dummy):
        while True:
            while self.jobIndex < len(self.jobs):
                job = self.jobs[self.jobIndex]
                if job.started:
                    continue
                job.started = True
                job.updateTime()
                job.setStatus("Running")
                o, pid = bf_popen(job.cmd)
                output = o.readline()
                while output:
                    job.output += output
                    output = o.readline()
                o.close()
                pid, sts = os.waitpid(pid, 0)
                sts = sts >> 8
                job.status = sts
                job.updateTime()
                job.output = job.output.rstrip()
                job.item.setToolTip(0, job.output)
                job.item.setToolTip(1, job.output)
                job.item.setToolTip(2, job.output)
                if job.status != 0:
                    job.setStatus("Failed")
                else:
                    job.setStatus("Done")
                self.jobIndex += 1
            time.sleep(1) # Ugly, fix. TODO

class Job():
    def __init__(self, fun, src, dst):
        self.fun = fun
        self.src = src
        self.dst = dst
        self.status = None
        self.output = ''
        self.started = False
        (self.cmd, self.cmdString) = self.fun(src,dst)

    def getCmdString(self):
        return self.cmdString

    def setStatus(self, string):
        self.item.setText(2, string)
        
    def updateTime(self):
        self.item.setText(0, time2str(timenow()))
