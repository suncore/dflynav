import os, stat, time
import _thread
from utils import *
from queue import Queue
if platform.system() == 'Windows':
    import pythoncom

class JobManager(object):
    def addJob(self, fun):
        _thread.start_new_thread(self.jobTask, (fun,))
    
    def jobTask(self, fun):
        try:
            if platform.system() == 'Windows':
                try:
                    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
                except pythoncom.com_error:
                    #already initialized.
                    pass
            fun()
        except:
            crash()

#class JobManager(object):
#    def __init__(self):
#        self.q = Queue()
#        thread.start_new_thread(self.jobTask, (self,))
#    
#    def addJob(self, fun):
#        self.q.put(fun)
#    
#    def jobTask(self, dummy):
#        try:
#            if platform.system() == 'Windows':
#                try:
#                    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
#                except pythoncom.com_error:
#                    #already initialized.
#                    pass
#            while True:
#                fun = self.q.get(True)
#                fun()
#        except:
#            crash()

