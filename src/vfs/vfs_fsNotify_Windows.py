
import os

import win32file
import win32event
import win32con
import thread


class Notify():
    def __init__(self):
        self.path = None
        thread.start_new_thread(self.notifyThread, (self,))
        #thread.start_new_thread(self.jobTask, (self,))

    def setNotify(self, path, cbfun):
        #print 'setnotify ' + path
        self.path = path
        self.cbfun = cbfun
        self.changeHandle = win32file.FindFirstChangeNotification (
              self.path,
              0,
              win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
              win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
              win32con.FILE_NOTIFY_CHANGE_SIZE |
              win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
              win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
        )

    def stop(self):
        if self.path:
            self.cbfun = None
            self.path = None
            win32file.FindCloseChangeNotification (self.changeHandle)

    def notifyThread(self, dummy):
        while 1:
            result = win32event.WaitForSingleObject (self.changeHandle, 500)
            if result == win32con.WAIT_OBJECT_0 and self.cbfun:
                self.cbfun()
            win32file.FindNextChangeNotification (self.changeHandle)

