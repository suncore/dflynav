
# VFS for normal file systems

import os, platform, shutil
import stat, time
import Df, fnmatch, Df_Dialog
if platform.system() == 'Windows':
    import ctypes, win32file, win32api, win32wnet, win32con
    import sys
    import win32com.client 
    from win32com.shell import shell, shellcon
from . import vfs_node
from utils import *
import subprocess, Df_Job, glob

if platform.system() != 'Windows':
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
else:
    unpackCmds = [
    [ ['tar', 'xzf'],
      ['tar.gz', 'tgz'] ],
    [ ['tar', 'xjf'],
      ['tar.bz2'] ],
    [ ['tar', 'xf'],
      ['tar'] ],
    [ ['#default'],
      ['zip', 'arj', 'cpio', 'deb', 'lzh', 'lha', 'lzma','rpm', 'cab', 'rar', '001', 'r00' ] ],
    [ ['#default'],
      ['gz'] ],
    [ ['#default'],
      ['bz2'] ],
    [ ['#default'],
      ['7z'] ]
    ]

pictureTypes = [ 'jpg', 'png', 'gif', 'tif' ]

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
            self.meta = [ ('Size', sizestr, self.size), 
                      ('Time', time2str(time.localtime(self.stat.st_mtime)), self.stat.st_mtime), 
                      ('Type', ext, ext),
                      ('Flags', flags, flags),
                      ('Size in bytes', str(self.size), self.size), 
                      ]
        if linkTarget:
            self.meta.append(('Link target', linkTarget, linkTarget))
        self.actionButtonCallbacks = [ 
                     ( 'Copy', True, self.cb_copy ),
                     ( 'Move', True, self.cb_move ),
                     ( 'Rename', False, self.cb_rename ),
                     ( 'Delete', False, self.cb_delete ),
                     ( 'Link', True, self.cb_link ),
                     #( 'Compare', True, self.cb_compare ),
                     ( 'Properties', True, self.cb_properties ),
                     ]
        self.wm = None

    def binaryOpCompat(self, obj):
        return isinstance(obj, Fs)
    
    def mkdir(self, dir):
        cmd = ['/bin/mkdir', path_join(self.fspath, dir)]
        cmdString = '$ mkdir %s' % path_join(self.fspath, dir)
        args = cmd, None
        Df.d.jobm.addJob(self.jobExecuter, args, cmdString)
        
    def fsFree(self):
        try:
            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(self.fspath), None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes))
                return free_bytes.value
            else:
                stat = os.statvfs(self.fspath)
                return stat.f_bavail * stat.f_bsize
        except:
            return None

    def open(self):
        error = None
        try:
            if platform.system() == 'Windows':
                os.startfile(genericPathToWindows(self.fspath))
            else:
                #os.chdir(self.parent.fspath)
                subprocess.call(["xdg-open", self.fspath]) # TODO should run completely async
        except:
            t,error,tb = sys.exc_info()
        if error:
            error = str(error)
        Df.d.jobm.addJobDone("$ open: " + self.fspath, error)

 
    def ops_compare(self, src, dst):
        pass
    
    def jobExecuter(self, args):
        return Cmd(args)
    
    def cb_copy(self):
        srcNodeList, dstNode = self.getSelectionAndDestination()
        if not srcNodeList:
            return
        srcList = [x.fspath for x in srcNodeList]
        cmd = [ '/bin/cp', '-drx' ] + srcList + [ dstNode.fspath ]
        srcList2 = [x.fsname for x in srcNodeList]
        srcs = ', '.join(srcList2)
        wd = srcNodeList[0].parent.fspath
        cmdString = '$ in %s: copy %s to %s' % (wd, srcs, dstNode.fspath)
        args = cmd, wd
        if platform.system() == 'Windows' and not Df.d.config.useInternalFileCopy:
            Df.d.jobm.addJobDone(cmdString, None)
            srcs = '\0'.join(srcList)
            #flag = shellcon.FOF_RENAMEONCOLLISION
            flag = 0
            shell.SHFileOperation (
              (0, shellcon.FO_COPY, genericPathToWindows(srcs), genericPathToWindows(dstNode.fspath), flag, None, None)
            )
            return
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
        cmdString = '$ in %s: move %s to %s' % (wd, srcs, dstNode.fspath)
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
            cmdString = '$ in %s: rename %s to %s' % (wd, src.fsname, newname)
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
        cmdString = '$ in %s: delete %s' % (wd, srcs)
        args = cmd, wd
        r = True
        if Df.d.config.confirmDelete:
            r = Df_Dialog.YesNo("Confirm", "Are you sure you want to delete the following files in " + wd + "?\n" + srcs)
        if r:
            Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_link(self):
        srcNodeList, dstNode = self.getSelectionAndDestination()
        for i in srcNodeList:
            cmd = [ '/bin/ln', '-s' ] + [ i.fspath ] + [ dstNode.fspath ]
            cmdString = '$ link %s to %s' % (i.fspath, dstNode.fspath)
            args = cmd, None
            if platform.system() == 'Windows':
                error = None
                try:
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(genericPathToWindows(dstNode.fspath + '/' + i.name + '.lnk'))
                    shortcut.Targetpath = genericPathToWindows(i.fspath)
                    #shortcut.Arguments = 'http://mysite.com/auth/preauth.php'
                    #shortcut.WorkingDirectory = r'C:\Program Files\Mozilla Firefox'
                    shortcut.save()
                except:
                    t,error,tb = sys.exc_info()
                if error:
                    error = str(error)
                Df.d.jobm.addJobDone(cmdString, error)
            else: 
                Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_dirsize(self):
        srcNodeList, x_ = self.getSelectionAndDestination()
        if not srcNodeList:
            return
        srcList = [x.fspath for x in srcNodeList]
        cmd = [ '/bin/du', '-sh' ] + srcList
        srcList = [x.fsname for x in srcNodeList]
        srcs = ', '.join(srcList)
        wd = srcNodeList[0].parent.fspath
        cmdString = '$ in %s: sizing %s' % (wd, srcs)
        args = cmd, wd
        Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_properties(self):
        srcNodeList, x_ = self.getSelectionAndDestination()
        if not srcNodeList:
            return
        WindowsOpenProperties(srcNodeList[0].fspath)

    def cb_pack(self):
        srcNodeList, x_ = self.getSelectionAndDestination()
        for i in srcNodeList:
            if platform.system() == 'Windows':
                cwd = os.getcwd()
                files = []
                try:
                    os.chdir(i.fspath)
                    files = glob.glob('*')
                except:
                    pass
                os.chdir(cwd)
                if files == []:
                    continue
                cmd = [ "src/res/7z.exe",  "a", "-bd", "-y", "-r" ] + [ i.fspath + '.zip' ] + files
                wd = i.fspath
            else:
                wd = i.parent.fspath
                cmd = [ 'zip', '-r' ] + [ i.fsname + '.zip' ] + [ i.fsname ]
            cmdString = '$ in %s: pack %s' % (wd, i.fsname)
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
                        if platform.system() == 'Windows':
                            if cmd == ['#default']:
                                a,b = os.path.splitext(srcNode.fsname)
                                cmd = [ "src/res/7z.exe", "x", "-bd", "-y", "-o"+a ]
                                cmd = cmd + [ srcNode.fspath ]
                            else:
                                cmd = cmd + [ windows2cygwinpath(srcNode.fspath) ]
                        else:
                            pass
                        cmdString = '$ unpack %s to %s' % (srcNode.fspath, dstNode.fspath)
                        wd = dstNode.fspath
                        args = cmd, wd
                        Df.d.jobm.addJob(self.jobExecuter, args, cmdString)

    def cb_compare(self):
        srcList, dst = self.getSelectionAndDestination()
        Df.d.jobm.addJobs(srcList[0].ops_compare, srcList, dst)
        
    def cb_openwith(self):
        srcList, dst = self.getSelectionAndDestination()
        if not srcList:
            return
        #Rundll32.exe shell32.dll, OpenAs_RunDLL C:\test.jpg
        p = srcList[0].fspath
        if platform.system() == 'Windows': 
            p = genericPathToWindows(p)
            subprocess.call(["Rundll32.exe", "shell32.dll", ",", "OpenAs_RunDLL", p]) # TODO exception handling
        else:
            subprocess.call(["src/df_openwith", p]) # TODO use other path

#    def cb_open(self):
#        srcList, dst = self.getSelectionAndDestination()
#        try:
#            if platform.system() == 'Windows':
#                fspathL = [ genericPathToWindows(n.fspath) for n in srcList ]
#                fspaths = ' '.join(fspathL)
#                os.startfile(fspaths)
#            else:
#                os.chdir(self.parent.fspath)
#                subprocess.call(["xdg-open", self.fsname]) # TODO should run completely async
#        except:
#            pass

class Directory(Fs):
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(Directory, self).__init__(parent, name, fsname, stats, linkTarget)
        if self.stat != None:
            self.meta[0] = ('Size', '-', 0L)
            self.meta[4] = ('Size in bytes', '-', 0L)
        self.actionButtonCallbacks.append(( 'Pack', False, self.cb_pack ))
        #self.actionButtonCallbacks.append(( 'Size', False, self.cb_dirsize ))
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
        
    def children(self, async=True):
        #print "1 ", self.childrenReady, self.children_
        if not async:
            self.getChildrenAsync(async)
        return self.children_

    def buildChild(self, f, stats):
        (st,attrib) = stats
        ext = fsPathExt(f)

        if platform.system() == 'Windows':
            if ext == 'lnk':
                linkTarget = self.getLinkTarget(path_join(self.fspath, f))
                #print linkTarget
                linkTargetStat = self.statFile(linkTarget)
                (linkTargetSt, linkTargetAttrib) = linkTargetStat
                if linkTarget[0:2] == '\\\\':
                    linkTarget = '/Network/'+windowsPathToGeneric(linkTarget)[2:]
                else:
                    linkTarget = '/Drives/'+windowsPathToGeneric(linkTarget)
                if linkTargetSt and stat.S_ISDIR(linkTargetSt.st_mode):
                    return Directory(self, f[:-4], f, stats, linkTarget)
                else:
                    return File(self, f[:-4], f, stats, linkTarget)
        else:
            if st and stat.S_ISLNK(st.st_mode):
                linkTarget = self.getLinkTarget(path_join(self.fspath, f))
                linkTargetStat = self.statFile(linkTarget)
                (linkTargetSt, linkTargetAttrib) = linkTargetStat
                linkTarget = '/Files/Local'+linkTarget
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
        try:
            if platform.system() == 'Windows':
                attrib = win32api.GetFileAttributes(path)
        except:
            pass
        return (st, attrib)


    def getLinkTarget(self,f):                
        #if True:
        if platform.system() == 'Windows':
            try:
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(genericPathToWindows(f))
                return shortcut.Targetpath
            except:
                pass
        else:
            try:
                #target = os.readlink(f)
                return os.path.realpath(f)
            except:
                pass
        return None
    
    def getChildrenAsync(self, async=True):
        c = []
        #if True:
        try:
            for f in os.listdir(self.fspath):
                if self.stopAsync:
                    break
                if platform.system() != 'Windows':
                    f = f.decode('utf-8','replace')
                #f = str(fn)
                try:
                    pj = path_join(self.fspath, f)
                except:
                    continue
                stats = self.statFile(pj)
                #stats = self.statFile(os.path.join(self.fspath, f))
                hide = f[0] == '.'
                if platform.system() == 'Windows':
                    (st, attrib) = stats
                    # todo configurable settings
                    #Df.d.config.win32_show_hidden
                    hide = hide or win32con.FILE_ATTRIBUTE_HIDDEN & attrib
                    #hide = hide or win32con.FILE_ATTRIBUTE_SYSTEM & attrib
                if not hide or Df.d.config.showHidden:
                    c.append(self.buildChild(f, stats))
        except:
            pass
        self.children_ = c
        #print "2", self.children_
        self.childrenReady = True
        self.asyncRunning = False
        self.stopAsync = False
        if async:
            Df.d.refresh.refreshSig.emit()
 
    def startMonitor(self, index):
        Df.d.fsNotify[index].setNotify(self.fspath, self.changeNotify_)

    def changeNotify_(self):
        #print "change"
        self.changed = True
        Df.d.refresh.refreshSig.emit()

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

    class WinNetworkServer(Directory):
        def __init__(self, parent, name, fsname):
            super(WinNetworkServer, self).__init__(parent, name, fsname)
    
        def childByName(self, name):
            return WinNetworkRoot(self, name, name)
        
        def startGetChildren(self):
            self.childrenReady = True
            Df.d.refresh.refreshSig.emit()
   
        def childrenStop(self):
            pass

        def children(self, async=True):
            return []
    
    class WinNetworkRoot(Directory):
        def __init__(self, parent, name, fsname):
            super(WinNetworkRoot, self).__init__(parent, name, fsname)

        def childByName(self, name):
            return Directory(self, name, name)

else:
    class RootDirectory(Directory):
        def __init__(self, parent, name, fsname):
            super(RootDirectory, self).__init__(parent, name, fsname)
            self.actionButtonCallbacks = []




class File(Fs):
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(File, self).__init__(parent, name, fsname, stats, linkTarget)
        #self.actionButtonCallbacks.insert(0,( 'Open', False, self.cb_open ))
        self.actionButtonCallbacks.append(( 'Open...', False, self.cb_openwith ))

    def icon(self):
        return Df.d.iconFactory.getFileIcon(self.fspath)

    def leaf(self):
        return True

class PackedFile(File):
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(PackedFile, self).__init__(parent, name, fsname, stats, linkTarget)
        self.actionButtonCallbacks.append(( 'Unpack', False, self.cb_unpack ))

class PictureFile(File):
    def __init__(self, parent, name, fsname, stats=None, linkTarget=None):
        super(PictureFile, self).__init__(parent, name, fsname, stats, linkTarget)
        self.actionButtonCallbacks.append(( 'Unpack', False, self.cb_unpack ))
            
    def preview(self):
        return ImageToPixmap(self.fspath)

    def icon(self):
        self.bigIcon = False
        if not Df.d.config.showThumbs:
            #self.icon_ = Df.d.iconFactory.getFileIcon(self.fspath)
            self.icon_ = super(PictureFile, self).icon()
        else:
            (iconData, date, dateSecs) = JpegThumbToIcon(self.fspath)
            if not iconData:
                #self.icon_ = Df.d.iconFactory.getFileIcon(self.fspath)
                self.icon_ = super(PictureFile, self).icon()
            else:
                self.bigIcon = True
                self.iconData, self.icon_ = iconData
                self.meta.append(("Taken", date, dateSecs))
        return self.icon_
    
    def hover(self, enter):
        print "Hover ", enter


class Cmd(Df_Job.Cmd):
    def __init__(self, args):
        cmd, workingDir = args
        self.error = None
        si = None
        if platform.system() == 'Windows':
            if os.path.exists("cygwin"):
                p = "cygwin"
            else:
                p = "c:/cygwin"
            if cmd[0][0] == '/':
                cmd2 = p + cmd[0]
            else:
                cmd2 = cmd[0]
            cmd = [cmd2] + cmd[1:]
            si = subprocess.STARTUPINFO()
            #si.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
            si.dwFlags = subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
        try:
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
        if platform.system() != 'Windows':
            time.sleep(2) # Ugly but good enough
            self.pob.kill()
        
    
