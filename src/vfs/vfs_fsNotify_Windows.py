
import os, time

import win32file
import win32event
import win32con
import thread


class Notify():
    def __init__(self):
        self.path = None
        self.changeHandle = None
        thread.start_new_thread(self.notifyThread, (self,))

    def setNotify(self, path, cbfun):
        #print 'setnotify ' + path
        self.stop()
        self.path = path
        self.cbfun = cbfun
        try:
            self.changeHandle = win32file.FindFirstChangeNotification(
              self.path,
              0,
              win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
              win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
              win32con.FILE_NOTIFY_CHANGE_SIZE |
              win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
              win32con.FILE_NOTIFY_CHANGE_LAST_WRITE)
        except:
            self.changeHandle = None

    def stop(self):
        if self.changeHandle:
            try:
                win32file.FindCloseChangeNotification(self.changeHandle)
            except:
                pass
            self.changeHandle = None

    def notifyThread(self, dummy):
        while 1:
            if self.changeHandle:
                try:
                    result = win32event.WaitForSingleObject(self.changeHandle, 1000)
                    if result == win32con.WAIT_OBJECT_0:
                        if self.cbfun:
                            self.cbfun()
                        #win32file.FindNextChangeNotificatio(self.changeHandle)
                except:
                    self.stop()
            else:
                time.sleep(1)

