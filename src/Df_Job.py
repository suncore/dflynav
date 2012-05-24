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

class JobManager():
    def __init__(self, jobsW):
        self.jobsW = jobsW
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
    
    def addJob(self, executer, args, cmdString):
        #item = QtGui.QTreeWidgetItem( [ '',  "<b>Hello</b> <i>Qt!</i>", "Queued" ] )
        item = QtGui.QTreeWidgetItem( [ '', cmdString, "Queued" ] )
        job = Job(args, executer, item)
        self.jobs.append(job)
        job.updateTime()
        self.jobsW.insertTopLevelItem(0, job.item)
        self.q.put(1)

    def jobTask(self, dummy):
        while True:
            x = self.q.get(True)
            while self.jobIndex < len(self.jobs):
                job = self.jobs[self.jobIndex]
                if job.started:
                    continue
                job.started = True
                job.updateTime()
                job.setStatus("Running")

                cmd = job.executer(job.args)
                output = cmd.readline()
                #print output
                while output:
                    # TOOD: Update tooltip while running
                    job.output += output
                    output = cmd.readline()
                    #print output
                job.status = cmd.finish()
                cmd = None
                job.updateTime()
                job.output = job.output.rstrip()
                job.item.setToolTip(0, job.output)
                job.item.setToolTip(1, job.output)
                job.item.setToolTip(2, job.output)
                #print job.output
                if job.status != 0:
                    job.setStatus("Failed")
                else:
                    job.setStatus("Done")
                self.jobIndex += 1

class Job():
    def __init__(self, args, executer, item):
        self.args = args
        self.executer = executer
        self.item = item
        
        self.status = None
        self.output = ''
        self.started = False

    def setStatus(self, string):
        self.item.setText(2, string)
        
    def updateTime(self):
        self.item.setText(0, time2str(timenow()))
