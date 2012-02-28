
import os
import stat, time
import pyinotify
from pyinotify import WatchManager, Notifier, ProcessEvent, ThreadedNotifier


class ProcessNotifyEvents(ProcessEvent):
    def process_IN_CREATE(self, event):
        #print 'process_IN_CREATE ' + event.path
        self.cbfun()
    def process_IN_DELETE(self, event):
        #print 'process_IN_DELETE ' + event.path
        self.cbfun()
    def process_IN_MOVED_TO(self, event):
        #print 'process_IN_MOVED_TO ' + event.path
        self.cbfun()
    def process_IN_MOVED_FROM(self, event):
        #print 'process_IN_MOVED_FROM ' + event.path
        self.cbfun()
    def process_IN_MODIFY(self, event):
        #print 'process_IN_MODIFY ' + event.path
        self.cbfun()

class Notify():
    def __init__(self):
        self.wm = WatchManager()
        self.pe = ProcessNotifyEvents()
        self.notifier = ThreadedNotifier(self.wm, self.pe)
        self.notifier.start()
        self.path = None
        #thread.start_new_thread(self.jobTask, (self,))

    def setNotify(self, path, cbfun):
        #print 'setnotify ' + path
        if self.path:
            self.wm.rm_watch(list(self.wdd.values()))
        self.path = path
        self.pe.cbfun = cbfun # ugly...
        
        self.wdd = self.wm.add_watch(self.path, 
                          pyinotify.IN_CREATE | 
                          pyinotify.IN_DELETE |
                          pyinotify.IN_MOVED_TO |
                          pyinotify.IN_MOVED_FROM |
                          pyinotify.IN_MODIFY)

    def stop(self):
        if self.path:
            self.wm.rm_watch(list(self.wdd.values()))
        self.notifier.stop()

    def notifyThread(self):
        while 1:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()

