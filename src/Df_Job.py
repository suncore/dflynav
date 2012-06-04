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
        self.message("hej", None)
        self.jobstatusW.close.clicked.connect(self.closeClicked)

    def closeClicked(self):
        self.jobstatusW.hide()

    def addJob(self, executer, args, cmdString):
        job = Job(args, executer, cmdString, self.jobsW)
        job.setStatus("Queued")
        self.jobs.append(job)
        job.updateTime()
        self.q.put(1)

    def message(self, msg, error):
        msg = Message(msg, error, self.jobsW)
        msg.updateTime()
        if error:
            msg.setStatus("Failed")
            msg.setToolTip(error)
        else:
            msg.setStatus("Done")

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
                job.setToolTip(job.output)
                #print job.output
                if job.status != 0:
                    job.setStatus("Failed")
                else:
                    job.setStatus("Done")
                self.jobIndex += 1


    def mouseButtonPressed(self, item):
        self.jobstatusW.output.setPlainText(item.df_entry.output)
        self.jobstatusW.command.setText(item.df_entry.cmd)
        self.jobstatusW.status.setText(item.df_entry.statusString)
        self.jobstatusW.show()
        

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
        
    def updateTime(self):
        self.item.setText(0, time2str(timenow()))

    def setToolTip(self, msg):
        for i in range(0,3):
            self.item.setToolTip(i, msg)

class Job(Entry):
    def __init__(self, args, executer, cmdString, jobsW):
        super(Job, self).__init__(cmdString, jobsW)
        self.args = args
        self.executer = executer
        self.status = None
        self.started = False

class Message(Entry):
    def __init__(self, msg, error, jobsW):
        super(Message, self).__init__(msg, jobsW)
        self.msg = msg
        self.error = error

