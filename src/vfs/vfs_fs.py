
# VFS for normal file systems

import os, platform, shutil
import stat, time
import Df, fnmatch, Df_Dialog
if platform.system() == 'Windows':
    import ctypes, win32file, win32api, win32wnet

from . import vfs_node
from utils import *

def path_join(a,b):
    if a[-1] == '/':
        return a + b
    return a + '/' + b

def FsPath(n):
    if n.fsname != None:
        path = n.fsname
    else:
        path = ''
    n = n.parent
    while n and isinstance(n, Fs):
        #print(n.fsname, path)
        path = path_join(n.fsname,path)
        n = n.parent
    return path


class Fs(vfs_node.Node):
    def __init__(self, parent, name, fsname):
        super(Fs, self).__init__(parent, name)
        self.fsname = fsname
        self.fspath = FsPath(self)
        try:
            self.stat = os.lstat(self.fspath)
            self.size = iff(stat.S_ISDIR(self.stat.st_mode), 0L, self.stat.st_size)
            self.meta = [ ('Size', iff(stat.S_ISDIR(self.stat.st_mode), '-', size2str(self.stat.st_size)), self.size), 
                      ('Date', time2str(time.localtime(self.stat.st_mtime)), self.stat.st_mtime), 
                      ]
        except:
            pass
        self.actionButtonCallbacks = [ 
                     ( 'Copy', True, self.cb_copy ),
                     ( 'Move', True, self.cb_move ),
                     ( 'Rename', False, self.cb_rename ),
                     ( 'Delete', False, self.cb_delete ),
                     ( 'Link', True, self.cb_link ),
                     ( 'Compare', True, self.cb_compare ),
                     ]
        self.wm = None

    def binaryOpCompat(self, obj):
        return isinstance(obj, Fs)
    
    def mkdir(self, dir):
        Df.d.jobm.addJobs(self.ops_mkdir, [ dir ], None)
        
    def fsFree(self):
        #try:
            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(self.fspath), None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes))
                return free_bytes.value
            else:
                stat = os.statvfs(self.fspath)
                return stat.f_bavail * stat.f_bsize
        #except:
            #return None


    # -------------------------------------------------------------------------------
    def ops_copy(self, src, dst):
        cmd = ('/bin/cp', '-drx', src.fspath, dst.fspath)
        cmdString = '$ copy %s to %s' % (toutf8(src.fspath), toutf8(dst.fspath))
        return (cmd, cmdString)

    def ops_move(self, src, dst):
        cmd = ('/bin/mv', src.fspath, dst.fspath)
        cmdString = '$ move %s to %s' % (toutf8(src.fspath), toutf8(dst.fspath))
        return (cmd, cmdString)

    def ops_rename(self, src, newpath):
        cmd = ('/bin/mv', src.fspath, newpath)
        cmdString = '$ rename %s to %s' % (toutf8(src.fspath), toutf8(newpath))
        return (cmd, cmdString)

    def ops_mkdir(self, dir, dummy):
        cmd = ('/bin/mkdir', path_join(self.fspath, dir))
        cmdString = '$ mkdir %s' % (toutf8(path_join(self.fspath, dir)))
        return (cmd, cmdString)

    def ops_delete(self, src, dst):
        cmd = ('/bin/rm', '-rf', src.fspath)
        cmdString = '$ delete %s' % (toutf8(src.fspath))
        return (cmd, cmdString)
 
    def ops_link(self, src, dst):
        cmd = ('/bin/ln', '-s', src.fspath, dst.fspath)
        cmdString = '$ link %s to %s' % (toutf8(src.fspath), toutf8(dst.fspath))
        return (cmd, cmdString)

    def ops_pack(self, src, dst):
        cmd = ('zip', '-r', src.fspath + '.zip', src.fspath)
        cmdString = '$ pack %s' % (toutf8(src.fspath))
        return (cmd, cmdString)

    def ops_unpack(self, src, dst):
        cmd = ('unzip', '-o', '-qq', '-d', dst.fspath, src.fspath)
        cmdString = '$ unpack %s to %s' % (toutf8(src.fspath), toutf8(dst.fspath))
        return (cmd, cmdString)

    def ops_compare(self, src, dst):
        pass
    
    def cb_copy(self):
        srcList, dst = self.getSelectionAndDestination()
        Df.d.jobm.addJobs(srcList[0].ops_copy, srcList, dst)

    def cb_move(self):
        srcList, dst = self.getSelectionAndDestination()
        Df.d.jobm.addJobs(srcList[0].ops_move, srcList, dst)

    def cb_rename(self):
        srcList, dst = self.getSelectionAndDestination()
        for src in srcList:
            newpath = Df_Dialog.Dialog("Rename", "Enter new name                                                                                                                                       ", 
                                       src.name)
            if newpath == None:
                return
            if newpath == src.fspath:
                continue
            Df.d.jobm.addJobs(srcList[0].ops_rename, [ src ], 
                              path_join(src.parent.fspath, newpath))

    def cb_delete(self):
        srcList, dst = self.getSelectionAndDestination()
        Df.d.jobm.addJobs(srcList[0].ops_delete, srcList, dst)

    def cb_link(self):
        srcList, dst = self.getSelectionAndDestination()
        Df.d.jobm.addJobs(srcList[0].ops_link, srcList, dst)

    def cb_pack(self):
        srcList, dst = self.getSelectionAndDestination()
        Df.d.jobm.addJobs(srcList[0].ops_pack, srcList, dst)

    def cb_unpack(self):
        srcList, dst = self.getSelectionAndDestination()
        Df.d.jobm.addJobs(srcList[0].ops_unpack, srcList, dst)

    def cb_compare(self):
        srcList, dst = self.getSelectionAndDestination()
        Df.d.jobm.addJobs(srcList[0].ops_compare, srcList, dst)


class Directory(Fs):
    def __init__(self, parent, name, fsname):
        super(Directory, self).__init__(parent, name, fsname)
        self.actionButtonCallbacks.append(( 'Pack', False, self.cb_pack ))
        self.stopAsync = False
        self.children_ = []
        self.asyncRunning = False
        self.childrenReady = False
        self.changed = False

    def startGetChildren(self):
        #print "startgetchildren"
        if not self.asyncRunning:
            self.asyncRunning = True
            self.childrenReady = False
            Df.d.vfsJobm.addJob(self.getChildrenAsync)
        
    def children(self):
        #print "1 ", self.childrenReady, self.children_
        return self.children_

    def buildChild(self, f):
        st = os.lstat(path_join(self.fspath, f))
        if stat.S_ISDIR(st.st_mode):
            c = Directory(self, f, f)
        else:
            if fnmatch.fnmatch(f, "*.zip"):
                c = PackedFile(self, f, f)
            else:
                c = File(self, f, f)
        return c
    
    def childByName(self, name):
        try:
            c = self.buildChild(name)
        except:
            c = None
        return c
        
    def childrenStop(self):
        if self.asyncRunning:
            self.stopAsync = True
        
    def getChildrenAsync(self):
        c = []
        try:
            for f in os.listdir(self.fspath):
                if self.stopAsync:
                    break
                if not f[0] == '.':
                    c.append(self.buildChild(f))
        except:
            pass
        self.children_ = c
        #print "2", self.children_
        self.childrenReady = True
        self.asyncRunning = False
        self.stopAsync = False
 
    def startMonitor(self, index):
        Df.d.fsNotify[index].setNotify(self.fspath, self.changeNotify_)

    def changeNotify_(self):
        #print "change"
        self.changed = True

if platform.system() == 'Windows':
    class WinDrive(Directory):
        def __init__(self, parent, name, fsname):
            super(WinDrive, self).__init__(parent, name, fsname)
            self.actionButtonCallbacks = []
            try:
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(self.fspath), None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes))
                drive= name+'\\'
                dt=win32file.GetDriveType(drive)
                netlabel = None
                if dt == win32file.DRIVE_UNKNOWN:
                    dts = ''
                if dt == win32file.DRIVE_NO_ROOT_DIR:
                    dts = ''
                if dt == win32file.DRIVE_REMOVABLE:
                    dts = 'Removable'
                if dt == win32file.DRIVE_FIXED:
                    dts = 'Fixed'
                if dt == win32file.DRIVE_REMOTE:
                    dts = 'Network'
                    try:
                        netlabel = win32wnet.WNetGetUniversalName(drive)
                    except:
                        pass
                if dt == win32file.DRIVE_CDROM:
                    dts = 'CD/DVD'
                if dt == win32file.DRIVE_RAMDISK:
                    dts = 'RAM'
                info = ('','','','','')
                try:
                    info = win32api.GetVolumeInformation(drive)
                except:
                    pass
                if netlabel:
                    label = netlabel
                else:
                    label = info[0]
                self.meta = [ ('Description', label, label), ('File System', info[4], info[4]), ('Type', dts, dts), ('Size', size2str(total_bytes.value), total_bytes.value), ('Free', size2str(free_bytes.value), free_bytes.value) ]
            except:
                pass
else:
    class RootDirectory(Directory):
        def __init__(self, parent, name, fsname):
            super(RootDirectory, self).__init__(parent, name, fsname)
            self.actionButtonCallbacks = []




class File(Fs):
    def leaf(self):
        return True

class PackedFile(File):
    def __init__(self, parent, name, fsname):
        super(PackedFile, self).__init__(parent, name, fsname)
        self.actionButtonCallbacks.append(( 'Unpack', False, self.cb_unpack ))
