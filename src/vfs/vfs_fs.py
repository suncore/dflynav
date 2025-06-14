
# VFS for normal file systems

import os, platform, shutil
import stat, time
import Df, fnmatch, Df_Dialog
from . import vfs_node
from utils import *
import subprocess, Df_Job, glob
import pwd, grp

unpackCmds = [
[ ['tar', 'xzf'],
    ['tar.gz', 'tgz'] ],
[ ['tar', 'xjf'],
    ['tar.bz2'] ],
[ ['tar', 'xf'],
    ['tar'] ],
[ ['unzip', '-oqq'],
    ['zip'] ],
[ ['gzip', '-d'],
    ['gz'] ],
[ ['bzip2', '-d'],
    ['bz2'] ],
[ ['7za', 'x'],
    ['7z'] ],
[ ['rar', 'x', '-o+'],
    ['rar', '001' ] ]
]

pictureTypes = [ 'jpg', 'png', 'gif', 'tif', 'heic', 'heif', 'avif' ]

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
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(Fs, self).__init__(parent, name)
        self.fsname = fsname
        self.fspath = FsPath(self)
        self.linkTarget = linkTarget
        if stats == None:
            if not isinstance(parent, Fs):
                stats = self.statFile(self.fsname)
            else:   
                stats = self.statFile(path_join(parent.fspath, self.fsname))
        (self.stat, self.attrib) = stats
        ext = fsPathExt(self.fsname)
        if linkTarget:
            ext = 'link'
        if self.stat != None:
            self.size = self.stat.st_size
            sizestr = size2str(self.stat.st_size)
            flags = mode2str(stats)
            uidgid = str(self.stat.st_uid) + "." + str(self.stat.st_gid)
            #import time
            #print(time.strftime("%x %X",time.localtime(time.time())))
            try:
                self.owner = Df.d.uidgrpCache[uidgid]
                # print("cache hit: " + uidgid + ":" + self.owner)
            except:
                try:
                    gidname = grp.getgrgid(self.stat.st_gid).gr_name
                except:
                    gidname = str(self.stat.st_gid)
                try:
                    uidname = pwd.getpwuid(self.stat.st_uid).pw_name
                except:
                    uidname = str(self.stat.st_uid)
                Df.d.uidgrpCache[uidgid] = self.owner = uidname + "." + gidname
                # print("cache miss: " + uidgid + ":" + self.owner)
            self.meta = [ ('Size', sizestr, self.size), 
                      ('Time', time2str(time.localtime(self.stat.st_mtime)), self.stat.st_mtime), 
                      ('Type', ext, ext),
                      ('Flags', flags, flags),
                      ('Size in bytes', str(self.size), self.size), 
                      ('Owner.Group', str(self.owner), self.owner), 
                      ]
        if linkTarget:
            self.meta.append(('Link target', linkTarget, linkTarget))
        self.actionButtonCallbacks = [ 
                     ( 'Copy', True, self.cb_copy ),
                     ( '   Copy As...   ', True, self.cb_copyas ),
                     ( 'Move', True, self.cb_move ),
                     ( 'Rename...', False, self.cb_rename ),
                     ( 'Delete', False, self.cb_delete ),
                     ( 'Softlink', True, self.cb_link ),
                     ( 'Diff', True, self.cb_compare ),
                     ( 'Size of', True, self.cb_properties ),
                     ]
        self.wm = None

    def binaryOpCompat(self, obj):
        return isinstance(obj, Fs)

    def mkdirDialog(self):
        newname = Df_Dialog.Dialog("Make Directory", "Enter name of new directory                                                                                                                                      ", 
                                    "")
        if newname == None:
            return
        self.mkdir(newname)

    def mkdir(self, dir):
        cmd = ['/bin/mkdir', path_join(self.fspath, dir)]
        cmdString = '$ mkdir %s' % path_join(self.fspath, dir)
        args = cmd, None
        Df.d.jobm.addJob(self.jobExecuter, args, cmdString)
        
    def fsFree(self):
        try:
            stat = os.statvfs(self.fspath)
            return stat.f_bavail * stat.f_bsize
        except:
            return None

    def open(self):
        # cmd = [ 'xdg-open', self.fspath ]
        # wd = self.parent.fspath
        # cmdString = '%s $ open %s' % (wd, self.fspath)
        # args = cmd, wd
        # Df.d.jobm.addJob(self.jobExecuter, args, cmdString)
        error = None
        try:
            #os.chdir(self.parent.fspath)
            subprocess.Popen(["xdg-open", self.fspath]) 
        except:
            t,error,tb = sys.exc_info()
        if error:
            error = str(error)
        Df.d.jobm.addJobDone("$ xdg-open " + self.fspath, error)
    
    def jobExecuter(self, args):
        return Cmd(args)
    
    def cb_copy(self):
        srcNodeList, dstNode = self.getSelectionAndDestination()
        if not srcNodeList:
            return
        srcList = [x.fspath for x in srcNodeList]
        cmd = [ '/bin/cp', '-rL' ] + srcList + [ dstNode.fspath ]
        srcList2 = [x.fsname for x in srcNodeList]
        srcs = ', '.join(srcList2)
        wd = srcNodeList[0].parent.fspath
        cmdString = '%s $ copy %s to %s' % (wd, srcs, dstNode.fspath)
        args = cmd, wd
        Df.d.jobm.addJob(self.jobExecuter, args, cmdString)
        
    def cb_copyas(self):
        srcList, dst = self.getSelectionAndDestination()
        for src in srcList:
            suggested = src.fsname
            newname = Df_Dialog.Dialog("Copy As", "Enter destination name                                                                                                                                       ", 
                                       suggested)
            if newname == None:
                return
            newname = path_join(dst.fspath, newname)
            wd = src.parent.fspath
            cmd = [ '/bin/cp', '-r', src.fspath, newname ]
            cmdString = '%s $ copyas %s to %s' % (wd, src.fsname, newname)
            args = cmd, wd
            Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_move(self):
        srcNodeList, dstNode = self.getSelectionAndDestination()
        if not srcNodeList:
            return
        srcList = [x.fspath for x in srcNodeList]
        cmd = [ '/bin/mv' ] + srcList + [ dstNode.fspath ]
        srcList = [x.fsname for x in srcNodeList]
        srcs = ', '.join(srcList)
        wd = srcNodeList[0].parent.fspath
        cmdString = '%s $ move %s to %s' % (wd, srcs, dstNode.fspath)
        args = cmd, wd
        Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_rename(self):
        srcList, dst = self.getSelectionAndDestination()
        for src in srcList:
            newname = Df_Dialog.Dialog("Rename", "Enter new name                                                                                                                                       ", 
                                       src.fsname)
            if newname == None:
                return
            if newname == src.fsname:
                continue
            wd = src.parent.fspath
            newpath = path_join(wd, newname)
            cmd = ['/bin/mv', src.fspath, newpath]
            cmdString = '%s $ rename %s to %s' % (wd, src.fsname, newname)
            args = cmd, wd
            Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_delete(self):
        srcNodeList, x_ = self.getSelectionAndDestination()
        if not srcNodeList:
            return
        srcList = [x.fspath for x in srcNodeList]
        cmd = [ '/bin/rm', '-rf' ] + srcList
        srcList = [x.fsname for x in srcNodeList]
        srcs = ', '.join(srcList)
        wd = srcNodeList[0].parent.fspath
        cmdString = '%s $ delete %s' % (wd, srcs)
        args = cmd, wd
        r = True
        if Df.d.config.confirmDelete:
            r = Df_Dialog.YesNo("Confirm", "Are you sure you want to delete the following files in " + wd + "?\n" + srcs)
        if r:
            Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_link(self):
        srcNodeList, dstNode = self.getSelectionAndDestination()
        if not srcNodeList:
            return
        srcList = [x.fspath for x in srcNodeList]
        cmd = [ '/bin/ln', '-s' ] + srcList + [ dstNode.fspath ]
        srcList = [x.fsname for x in srcNodeList]
        srcs = ', '.join(srcList)
        wd = srcNodeList[0].parent.fspath
        cmdString = '%s $ link %s to %s' % (wd, srcs, dstNode.fspath)
        args = cmd, wd
        #print args
        #print cmdString
        Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_properties(self):
        srcNodeList, x_ = self.getSelectionAndDestination()
        if not srcNodeList:
            return
        srcList = [x.fspath for x in srcNodeList]
        cmd = [ '/bin/du', '-sch', '--apparent-size' ] + srcList
        srcList = [x.fsname for x in srcNodeList]
        srcs = ', '.join(srcList)
        wd = srcNodeList[0].parent.fspath
        cmdString = '%s $ size of %s' % (wd, srcs)
        args = cmd, wd
        Df.d.jobm.addJob(self.jobExecuter, args, cmdString, showStatusNow=True)

    def cb_pack(self):
        srcNodeList, x_ = self.getSelectionAndDestination()
        for i in srcNodeList:
            wd = i.parent.fspath
            cmd = [ 'zip', '-r' ] + [ i.fsname + '.zip' ] + [ i.fsname ]
            cmdString = '%s $ zip %s' % (wd, i.fsname)
            args = cmd, wd
            Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_unpack(self):
        srcNodeList, dstNode = self.getSelectionAndDestination()
        for srcNode in srcNodeList:
            ext = fsPathExt(srcNode.fspath)
            for i in unpackCmds:
                cmd, exts = i
                for e in exts:
                    if ext == e:
                        cmd = cmd + [ srcNode.fspath ]
                        cmdString = '$ unpack %s to %s' % (srcNode.fspath, dstNode.fspath)
                        wd = dstNode.fspath
                        args = cmd, wd
                        Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_compare(self):
        src, dst = self.getSelectionAndDestinationDiff()
        if len(src) != 1 or len(dst) != 1:
            Df_Dialog.MessageInfo("Diff","Please select only one item in each pane, then click the Diff button.")
            return
        wd = src[0].parent.fspath
        src = src[0].fspath
        dst = dst[0].fspath
        cmd = [ '/usr/bin/diff', '-r', src, dst ]
        cmdString = '%s $ diff %s %s' % (wd, src, dst)
        args = cmd, wd
        Df.d.jobm.addJob(self.jobExecuter, args, cmdString, showStatusNow=True, ignoreError=True)
        
    def cb_openwith(self):
        srcList, dst = self.getSelectionAndDestination()
        if not srcList:
            return
        p = "file://"+srcList[0].fspath
        #print(p)
        subprocess.Popen(["./openwith/openwith", p])

#    def cb_open(self):
#        srcList, dst = self.getSelectionAndDestination()
#        try:
#            os.chdir(self.parent.fspath)
#            subprocess.call(["xdg-open", self.fsname]) # TODO should run completely async
#        except:
#            pass

class Directory(Fs):
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(Directory, self).__init__(parent, name, fsname, stats, linkTarget)
        if self.stat != None:
            self.meta[0] = ('Size', '-', 0)
            self.meta[4] = ('Size in bytes', '-', 0)
        self.actionButtonCallbacks.append(( 'Zip', False, self.cb_pack ))
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
        
    def children(self, asynch=True):
        #print "1 ", self.childrenReady, self.children_
        if not asynch:
            self.getChildrenAsync(asynch)
        return self.children_

    def buildChild(self, f, stats):
        (st,attrib) = stats
        ext = fsPathExt(f)

        if st and stat.S_ISLNK(st.st_mode):
            linkTarget = self.getLinkTarget(path_join(self.fspath, f))
            linkTargetStat = self.statFile(linkTarget)
            (linkTargetSt, linkTargetAttrib) = linkTargetStat
            #linkTarget = '/Files/Local'+linkTarget
            if linkTargetSt and stat.S_ISDIR(linkTargetSt.st_mode):
                return Directory(self, f, f, stats, linkTarget)
            else:
                return File(self, f, f, stats, linkTarget)
        if st and stat.S_ISDIR(st.st_mode):
            return Directory(self, f, f, stats)
        for i in unpackCmds:
            cmd, exts = i
            for e in exts:
                if ext == e:
                    return PackedFile(self, f, f, stats)
        for e in pictureTypes:
            if ext == e:
                return PictureFile(self, f, f, stats)
        return File(self, f, f, stats)
    
    def childByName(self, name):
        (st, attrib) = self.statFile(path_join(self.fspath, name))
        if st == None:
            return None
        return self.buildChild(name, (st, attrib))
        
    def childrenStop(self):
        if self.asyncRunning:
            self.stopAsync = True
    
    def statFile(self, path):
        st = None
        try:
            st = os.lstat(path)
        except:
            pass
        attrib = 0
        return (st, attrib)


    def getLinkTarget(self,f):                
        try:
            return os.path.realpath(f)
        except:
            pass
        return None
    
    def getChildrenAsync(self, asynch=True):
        c = []
        if True:
            try:
                for f in os.listdir(str(self.fspath)):
                    if self.stopAsync:
                        break
                    if not isinstance(f, str):
                        f = f.decode('utf-8',errors='replace')
                    pj = path_join(self.fspath, f)
                    stats = self.statFile(pj)
                    hide = f[0] == '.'
                    if not hide or Df.d.config.showHidden:
                        c.append(self.buildChild(f, stats))
            except Exception as e:
                #print("Exception trying to list " + str(self.fspath))
                print(e)
                pass
        self.children_ = c
        self.childrenReady = True
        self.asyncRunning = False
        self.stopAsync = False
        if asynch:
            Df.d.refresh.refreshSig.emit()
 
    def startMonitor(self, index):
        Df.d.fsNotify[index].setNotify(self.fspath, self.changeNotify_)

    def changeNotify_(self):
        #print "change"
        self.changed = True
        Df.d.refresh.refreshSig.emit()
        # time.sleep(1)

    def icon(self, fast):
        return Df.d.iconFactory.getFolderIcon(softlink=(self.linkTarget != None))


class RootDirectory(Directory):
    def __init__(self, parent, name, fsname):
        super(RootDirectory, self).__init__(parent, name, fsname)
        self.actionButtonCallbacks = []

class File(Fs):
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(File, self).__init__(parent, name, fsname, stats, linkTarget)
        #self.actionButtonCallbacks.insert(0,( 'Open', False, self.cb_open ))
        self.actionButtonCallbacks.append(( 'Open With...', False, self.cb_openwith ))

    def preview(self):
        return TextToPreview(self.fspath)

    def icon(self, fast):
        return Df.d.iconFactory.getFileIcon(self.fspath, softlink=(self.linkTarget != None))

    def leaf(self):
        return True

class PackedFile(File):
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(PackedFile, self).__init__(parent, name, fsname, stats, linkTarget)
        self.actionButtonCallbacks.append(( 'Unpack', False, self.cb_unpack ))

class PictureFile(File):
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(PictureFile, self).__init__(parent, name, fsname, stats, linkTarget)
        self.bigIcon = True
        self.actionButtonCallbacks.append(( 'Unpack', False, self.cb_unpack ))
            
    def preview(self):
        return ImageToPreview(self.fspath)

    def icon(self, fast):
        if fast or (not Df.d.config.showThumbs):
            #self.icon_ = Df.d.iconFactory.getFileIcon(self.fspath)
            self.icon_ = super(PictureFile, self).icon(fast)
        else:
            (iconData, date, dateSecs) = ImageToIcon(self.fspath)
            if not iconData:
                #self.icon_ = Df.d.iconFactory.getFileIcon(self.fspath)
                self.icon_ = super(PictureFile, self).icon(fast)
            else:
                # self.bigIcon = True
                self.iconData, self.icon_ = iconData
                self.meta.append(("Taken", date, dateSecs)) # TODO This is too late, the panel has already iterated over all children to find all meta...
        return self.icon_
    
    def hover(self, enter):
        print("Hover ", enter)


class Cmd(Df_Job.Cmd):
    def __init__(self, args):
        cmd, workingDir = args
        self.error = None
        si = None
        try:
            #print cmd
            if workingDir:
                self.pob = Popen(cmd, bufsize=1, stdout=PIPE, stderr=STDOUT, universal_newlines=True, cwd=workingDir, startupinfo=si)
            else:
                self.pob = Popen(cmd, bufsize=1, stdout=PIPE, stderr=STDOUT, universal_newlines=True, startupinfo=si)
        except:
            t,self.error,tb = sys.exc_info()
        if self.error:
            self.error = 'Command failed: "'+' '.join(cmd)+'"\nError code: '+str(self.error)+'\nThis usually means that the executable program '+cmd[0]+' could not be found to run the command.'
            
    def readline(self):
        return self.pob.stdout.readline()

    def finish(self):
        self.pob.wait()
        return self.pob.returncode

    def stop(self):
        self.pob.terminate()
        time.sleep(2) # Ugly but good enough
        self.pob.kill()
        
    
