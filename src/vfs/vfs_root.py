
import platform
from . import vfs_node, vfs_fs

class VfsRoot(vfs_node.Node):
    def __init__(self):
        super(VfsRoot, self).__init__(None, '/')
    def children(self):
        return [
            VfsRoot_Files(self, 'Files'),
            VfsRoot_Apps(self, 'Applications')
            ] 

class VfsRoot_Files(vfs_node.Node):
    def children(self):
        if platform.system() == 'Windows':
            import win32api
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            drivelist = [ vfs_fs.WinDrive(self, i[0:2], i[0:2]+'/') for i in drives ]
            return drivelist
        else:
            return [
                    vfs_fs.RootDirectory(self, 'Local', '/')
                    ] 


class VfsRoot_Apps(vfs_node.Node):
    def children(self):
        return [
            vfs_fs.Directory(self, 'Apps', '/')
            ] 

 
