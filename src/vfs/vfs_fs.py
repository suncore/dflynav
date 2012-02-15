
# VFS for normal file systems

import os
import stat, time
import Df, fnmatch

import vfs_node
from utils import *


def FsPath(n):
    if n.fsname <> None:
        path = n.fsname
    else:
        path = ''
    n = n.parent
    while n and isinstance(n, Fs):
        #print(n.fsname, path)
        path = os.path.join(n.fsname,path)
        n = n.parent
    return path


class Fs(vfs_node.Node):
    def __init__(self, parent, name, fsname):
        super(Fs, self).__init__(parent, name)
        self.fsname = fsname
        self.fspath = FsPath(self)
        self.stat = os.lstat(self.fspath)
        self.meta = [ ('Size', iff(stat.S_ISDIR(self.stat.st_mode), '-', size2str(self.stat.st_size)), iff(stat.S_ISDIR(self.stat.st_mode), 0, self.stat.st_size)), 
                      ('Date', time2str(time.localtime(self.stat.st_mtime)), self.stat.st_mtime), 
                      ]
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

    # -------------------------------------------------------------------------------
    def ops_copy(self, src, dst):
        # if Linux:
        cmd = ('/bin/cp', '-drx', src.fspath, dst.fspath)
        #cmd = ('/a/proj/dragonfly/src/testcmd', src.fspath, dst.fspath)
        # if Windows:
        # TODO
        cmdString = '$ copy %s %s' % (toutf8(src.fspath), toutf8(dst.fspath))
        return (cmd, cmdString)

    def ops_move(self, src, dst):
        cmd = ('/bin/mv', src.fspath, dst.fspath)
        cmdString = '$ move %s %s' % (toutf8(src.fspath), toutf8(dst.fspath))
        return (cmd, cmdString)

    def ops_rename(self, src, dst):
        pass

    def ops_delete(self, src, dst):
        cmd = ('/bin/rm', '-rf', src.fspath)
        cmdString = '$ delete %s' % (toutf8(src.fspath))
        return (cmd, cmdString)
 
    def ops_link(self, src, dst):
        cmd = ('/bin/ln', '-s', src.fspath, dst.fspath)
        cmdString = '$ link %s %s' % (toutf8(src.fspath), toutf8(dst.fspath))
        return (cmd, cmdString)

    def ops_pack(self, src, dst):
        cmd = ('zip', '-r', src.fspath + '.zip', src.fspath)
        cmdString = '$ pack %s' % (toutf8(src.fspath))
        return (cmd, cmdString)

    def ops_unpack(self, src, dst):
        cmd = ('unzip', '-o', '-qq', '-d', dst.fspath, src.fspath)
        cmdString = '$ unpack %s %s' % (toutf8(src.fspath), toutf8(dst.fspath))
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
        Df.d.jobm.addJobs(srcList[0].ops_rename, srcList, dst)

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

    def children(self):
        if True: #self.children_ == None: # TODO enable updates when contents change
            c = []
            for f in os.listdir(self.fspath):
            #try:
                if not f[0] == '.':
                    st = os.lstat(os.path.join(self.fspath, f))
                    if stat.S_ISDIR(st.st_mode):
                        c.append(Directory(self, f, f))
                    else:
                        if fnmatch.fnmatch(f, "*.zip"):
                            c.append(PackedFile(self, f, f))
                        else:
                            c.append(File(self, f, f))
            #except:
                #c.append(File(self, f, st))
            self.children_ = c
        return self.children_

    def startMonitor(self, index):
        self.fsChange = False
        Df.d.fsNotify[index].setNotify(self.fspath, self.changeNotify)

    def changeNotify(self):
        self.fsChange = True

    def changed(self):
        if self.fsChange:
            self.fsChange = False
            return True


class File(Fs):
    def leaf(self):
        return True

class PackedFile(File):
    def __init__(self, parent, name, fsname):
        super(PackedFile, self).__init__(parent, name, fsname)
        self.actionButtonCallbacks.append(( 'Unpack', False, self.cb_unpack ))
