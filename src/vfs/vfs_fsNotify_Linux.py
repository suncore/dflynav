
from inotify_simple import INotify, flags
import _thread, time

class Notify():
    def __init__(self):
        self.inotify = INotify()
        self.path = None
        self.wd = None
        self.cbfun = None
        _thread.start_new_thread(self.notifyThread,(self,))

    def setNotify(self, path, cbfun):
        self.stop()
        watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.MOVED_TO | flags.MOVED_FROM
        try:
            self.wd = self.inotify.add_watch(path, watch_flags)
        except:
            self.wd = None
        self.path = path
        self.cbfun = cbfun

    def stop(self):
        if self.wd:
            self.inotify.rm_watch(self.wd)
        self.wd = None
        self.path = None

    def notifyThread(self, dummy):
        while 1:
            evs1 = self.inotify.read() # blocking
            time.sleep(1)
            evs2 = self.inotify.read(timeout=0) # non-blocking to flush queue
            signal = False
            for event in evs1+evs2:
                for flag in flags.from_mask(event.mask):
                    if flag != flags.IGNORED:
                        signal = True
            if signal:
                self.cbfun()

# import pyinotify
# from pyinotify import WatchManager, Notifier, ProcessEvent, ThreadedNotifier


# class ProcessNotifyEvents(ProcessEvent):
#     def process_IN_CREATE(self, event):
#         #print 'process_IN_CREATE ' + event.path
#         self.cbfun()
#     def process_IN_DELETE(self, event):
#         #print 'process_IN_DELETE ' + event.path
#         self.cbfun()
#     def process_IN_MOVED_TO(self, event):
#         #print 'process_IN_MOVED_TO ' + event.path
#         self.cbfun()
#     def process_IN_MOVED_FROM(self, event):
#         #print 'process_IN_MOVED_FROM ' + event.path
#         self.cbfun()
#     def process_IN_MODIFY(self, event):
#         #print 'process_IN_MODIFY ' + event.path
#         self.cbfun()

# class Notify():
#     def __init__(self):
#         self.wm = WatchManager()
#         self.pe = ProcessNotifyEvents()
#         self.notifier = ThreadedNotifier(self.wm, self.pe)
#         self.notifier.start()
#         self.path = None
#         #thread.start_new_thread(self.jobTask, (self,))

#     def setNotify(self, path, cbfun):
#         #print 'setnotify ' + path
#         if self.path:
#             self.wm.rm_watch(list(self.wdd.values()))
#         self.path = path
#         self.pe.cbfun = cbfun # ugly...
#         #print sys.getfilesystemencoding()
#         self.wdd = self.wm.add_watch(self.path, 
#                           pyinotify.IN_CREATE | 
#                           pyinotify.IN_DELETE |
#                           pyinotify.IN_MOVED_TO |
#                           pyinotify.IN_MOVED_FROM |
#                           pyinotify.IN_MODIFY)

#     def stop(self):
#         if self.path:
#             self.wm.rm_watch(list(self.wdd.values()))
#         self.notifier.stop()

#     def notifyThread(self):
#         while 1:
#             notifier.process_events()
#             if notifier.check_events():
#                 notifier.read_events()

