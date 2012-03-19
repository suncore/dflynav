
import os, platform, shutil
import stat, time
import Df, fnmatch, Df_Dialog
import ctypes, win32file, win32api, win32wnet, win32con
from . import vfs_node
from utils import *
import sys
from _winreg import *


class InstalledDirectory(vfs_node.Node):
    def __init__(self, parent, name):
        super(InstalledDirectory, self).__init__(parent, name)

    def children(self):
        c = []
        aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
        oldname = ''
        for mode in ( KEY_WOW64_64KEY, KEY_WOW64_32KEY ):
            aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, KEY_READ | mode)
            (subkeys, values, time) = QueryInfoKey(aKey)
            for i in range(subkeys):
                try:
                    asubkey_name=EnumKey(aKey,i)
                    asubkey=OpenKey(aKey,asubkey_name)
                    k = {}
                    for n in ( "DisplayName", "DisplayIcon", "DisplayVersion", "Publisher", "UninstallString", "InstallDate" ):
                        k[n] = ''
                        try:
                            (k[n], regtype)=QueryValueEx(asubkey, n)
                        except:
                            pass
                    if k["DisplayName"] != '' and oldname != k["DisplayName"]:
                        for x in c:
                            if k["DisplayName"] == x.name:
                                break
                        else:
                            oldname = k["DisplayName"]
                            c.append(InstalledApplication(self,k["DisplayName"],k))
                except:
                    pass
        return c

class InstalledApplication(vfs_node.Node):
    def __init__(self, parent, name, k):
        super(InstalledApplication, self).__init__(parent, name)
        self.meta = [ ('Version',k['DisplayVersion'],k['DisplayVersion']), ('Publisher',k['Publisher'],k['Publisher']), ('Install Date',k['InstallDate'],k['InstallDate']) ]
    
    def leaf(self):
        return True
