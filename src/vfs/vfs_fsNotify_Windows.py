
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



import os

import win32file
import win32event
import win32con

path_to_watch = os.path.abspath (".")

#
# FindFirstChangeNotification sets up a handle for watching
#  file changes. The first parameter is the path to be
#  watched; the second is a boolean indicating whether the
#  directories underneath the one specified are to be watched;
#  the third is a list of flags as to what kind of changes to
#  watch for. We're just looking at file additions / deletions.
#
change_handle = win32file.FindFirstChangeNotification (
  path_to_watch,
  0,
  win32con.FILE_NOTIFY_CHANGE_FILE_NAME
)

#
# Loop forever, listing any file changes. The WaitFor... will
#  time out every half a second allowing for keyboard interrupts
#  to terminate the loop.
#
try:

  old_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
  while 1:
    result = win32event.WaitForSingleObject (change_handle, 500)

    #
    # If the WaitFor... returned because of a notification (as
    #  opposed to timing out or some error) then look for the
    #  changes in the directory contents.
    #
    if result == win32con.WAIT_OBJECT_0:
      new_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in new_path_contents if not f in old_path_contents]
      deleted = [f for f in old_path_contents if not f in new_path_contents]
      if added: print "Added: ", ", ".join (added)
      if deleted: print "Deleted: ", ", ".join (deleted)

      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification (change_handle)

finally:
  win32file.FindCloseChangeNotification (change_handle)
