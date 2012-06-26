import os, stat, time
import thread
from utils import *
from Queue import Queue
if platform.system() == 'Windows':
    import pythoncom

class JobManager(object):
    def __init__(self):
        self.q = Queue()
        thread.start_new_thread(self.jobTask, (self,))
    
    def addJob(self, fun):
        self.q.put(fun)
    
    def jobTask(self, dummy):
        try:
            if platform.system() == 'Windows':
                try:
                    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
                except pythoncom.com_error:
                    #already initialized.
                    pass
            while True:
                fun = self.q.get(True)
                fun()
        except:
            crash()

