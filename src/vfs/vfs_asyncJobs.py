import os, stat, time
import thread
from utils import *
from Queue import Queue

class JobManager(object):
    def __init__(self):
        self.q = Queue()
        thread.start_new_thread(self.jobTask, (self,))
    
    def addJob(self, fun):
        self.q.put(fun)
    
    def jobTask(self, dummy):
        while True:
            fun = self.q.get(True)
            fun()

