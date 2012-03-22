
import platform, os
from . import vfs_node, vfs_fs, vfs_apps_Windows

class VfsRoot(vfs_node.Node):
    def __init__(self):
        super(VfsRoot, self).__init__(None, '/')
    def children(self):
        if platform.system() == 'Windows':
            homepath = os.path.expanduser('~')
            homepath = '/'.join(homepath.split('\\'))
            #startmenupath = homepath + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
            return [
                VfsRoot_WinTopFolder(self, 'Home', homepath),
                VfsRoot_WinDrives(self, 'Drives'),
                #VfsRoot_Apps_Windows(self, 'Applications')
                #VfsRoot_WinTopFolder(self, 'Applications', startmenupath),
                ] 
        else:
            return [
                VfsRoot_Files(self, 'Files'),
                VfsRoot_Apps(self, 'Applications')
                ] 


class VfsRoot_WinTopFolder(vfs_fs.Directory):
    def __init__(self, parent, name, fsname):
        super(VfsRoot_WinTopFolder, self).__init__(parent, name, fsname)
        self.meta = []

class VfsRoot_WinDrives(vfs_node.Node):
    def children(self):
        import win32api
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        drivelist = [ vfs_fs.WinDrive(self, i[0:2], i[0:2]+'/') for i in drives ]
        return drivelist

class VfsRoot_Files(vfs_node.Node):
    def children(self):
        return [
                vfs_fs.RootDirectory(self, 'Local', '/')
                ] 


class VfsRoot_Apps(vfs_node.Node):
    def children(self):
        return [
            vfs_fs.Directory(self, 'Apps', '/')
            ] 

 
class VfsRoot_Apps_Windows(vfs_node.Node):
    def children(self):
        return [
            vfs_apps_Windows.InstalledDirectory(self, 'Installed')
            ] 

 
