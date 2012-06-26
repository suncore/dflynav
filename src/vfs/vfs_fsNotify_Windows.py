
import os, time

import win32file
import win32event
import win32con
import thread
from utils import *


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
        self.startTime = time.time()
        try:
            self.changeHandle = win32file.FindFirstChangeNotification(
              self.path,
              0,
              win32con.FILE_NOTIFY_CHANGE_FILE_NAME | 
              win32con.FILE_NOTIFY_CHANGE_DIR_NAME 
              #|
              #win32con.FILE_NOTIFY_CHANGE_SIZE |
              #win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
              #win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
              )
        except:
            self.changeHandle = None

    def stop(self):
        if self.changeHandle:
            hdl = self.changeHandle
            self.changeHandle = None
            try:
                win32file.FindCloseChangeNotification(hdl)
            except:
                pass

    def notifyThread(self, dummy):
        try:
            while 1:
                if self.changeHandle:
                    try:
                        result = win32event.WaitForSingleObject(self.changeHandle, 1000)
                        if result == win32con.WAIT_OBJECT_0 and self.changeHandle:
                            if self.cbfun: # and ((time.time() - self.startTime) > 0.1):
                                self.startTime = time.time()
                                self.cbfun()
                            win32file.FindNextChangeNotification(self.changeHandle)
                    except:
                        self.stop()
                else:
                    time.sleep(1)
        except:
            crash()


#class Notify():
#    def __init__(self):
#        self.path = None
#        self.changeHandle = None
#        thread.start_new_thread(self.notifyThread, (self,))
#
#    def setNotify(self, path, cbfun):
#        #print 'setnotify ' + path
#        self.stop()
#        self.path = path
#        self.cbfun = cbfun
#        try:
#            self.changeHandle = win32file.CreateFile (
#                self.path,
#                0x0001,
#                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
#                None,
#                win32con.OPEN_EXISTING,
#                win32con.FILE_FLAG_BACKUP_SEMANTICS,
#                None
#            )
#            pass
#        except:
#            self.changeHandle = None
#
#    def stop(self):
#        if self.changeHandle:
#            try:
#                win32file.CloseHandle(self.changeHandle)
#            except:
#                pass
#            self.changeHandle = None
#
#    def notifyThread(self, dummy):
#        while 1:
#            if self.changeHandle:
#                time.sleep(0.1)
#                try:
#                    results = win32file.ReadDirectoryChangesW (
#                                self.changeHandle,
#                                1024,
#                                False,
#                                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
#                                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
#                                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
#                                win32con.FILE_NOTIFY_CHANGE_SIZE |
#                                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
#                                None,
#                                None
#                              )
#                    if self.cbfun:
#                        self.cbfun()
#                except:
#                    self.stop()
#            else:
#                time.sleep(1)
#

