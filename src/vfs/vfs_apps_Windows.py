
import os, platform, shutil
import stat, time
import Df, fnmatch, Df_Dialog
import ctypes, win32file, win32api, win32wnet, win32con
from . import vfs_node
from utils import *
import sys
from _winreg import *


class Apps(vfs_node.Node):
    def children(self):
        return [
            UninstallDirectory(self, 'Uninstall')
            ] 

class UninstallDirectory(vfs_node.Node):
    def __init__(self, parent, name):
        super(UninstallDirectory, self).__init__(parent, name)

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
                            c.append(UninstallApplication(self,k["DisplayName"],k))
                except:
                    pass
        return c

class UninstallApplication(vfs_node.Node):
    def __init__(self, parent, name, k):
        super(UninstallApplication, self).__init__(parent, name)
        self.meta = [ ('Version',k['DisplayVersion'],k['DisplayVersion']), ('Publisher',k['Publisher'],k['Publisher']), ('Install Date',k['InstallDate'],k['InstallDate']) ]
    
    def leaf(self):
        return True
    
class Installed(vfs_node.Node):    
    def __init__(self, parent, name, k):
        super(UninstallApplication, self).__init__(parent, name)

            
            startmenupath = os.getenv("appdata")
            startmenupath = '/'.join(startmenupath.split('\\'))
            startmenupath = startmenupath + "/Microsoft/Windows/Start Menu/Programs"
            smp2 = os.getenv("programdata")
            smp2 = '/'.join(smp2.split('\\'))
            smp2 = smp2 + "/Microsoft/Windows/Start Menu/Programs"

