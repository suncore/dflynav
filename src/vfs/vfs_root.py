
import platform, os
from . import vfs_node, vfs_fs
if platform.system() == 'Windows':
    from . import vfs_apps_Windows
    import win32api
    

class VfsRoot(vfs_node.Node):
    def __init__(self):
        super(VfsRoot, self).__init__(None, '/')
    def children(self, async=True):
        if platform.system() == 'Windows':
            homepath = os.path.expanduser('~')
            homepath = '/'.join(homepath.split('\\'))
            return [
                VfsRoot_WinTopFolder(self, 'Home', homepath),
                VfsRoot_WinDrives(self, 'Drives'),
                VfsRoot_WinNetwork(self, 'Network'),
                #vfs_apps_Windows.Apps(self, 'Applications')
                ] 
        else:
            return [
                VfsRoot_Files(self, 'Files'),
                ] 


class VfsRoot_WinTopFolder(vfs_fs.Directory):
    def __init__(self, parent, name, fsname):
        super(VfsRoot_WinTopFolder, self).__init__(parent, name, fsname)
        self.meta = []

class VfsRoot_WinDrives(vfs_node.Node):
    def children(self, async=True):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        drivelist = [ vfs_fs.WinDrive(self, i[0:2], i[0:2]+'/') for i in drives ]
        return drivelist

class VfsRoot_WinNetwork(vfs_node.Node):
    def childByName(self, name):
        return vfs_fs.WinNetworkServer(self, name, '//'+name)

class VfsRoot_Files(vfs_node.Node):
    def children(self, async=True):
        return [
                vfs_fs.RootDirectory(self, 'Local', '/')
                ] 

