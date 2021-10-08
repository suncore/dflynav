import os, stat, time
import _thread
from utils import *
from queue import Queue

class JobManager(object):
    def addJob(self, fun):
        _thread.start_new_thread(self.jobTask, (fun,))
    
    def jobTask(self, fun):
        try:
            fun()
        except:
            crash()

