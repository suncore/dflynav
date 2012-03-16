
import platform
from . import vfs_node, vfs_fs

class VfsRoot(vfs_node.Node):
    def __init__(self):
        super(VfsRoot, self).__init__(None, '/')
    def children(self):
        if platform.system() == 'Windows':
            return [
                vfs_fs.WinHome(self, 'Home', 'C:/Users/hch'),
                VfsRoot_WinDrives(self, 'Drives'),
                VfsRoot_Apps(self, 'Applications')
                ] 
        else:
            return [
                VfsRoot_Files(self, 'Files'),
                VfsRoot_Apps(self, 'Applications')
                ] 

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

 
