
import vfs_node, vfs_fs

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
        return [
            vfs_fs.Directory(self, 'Local', '/')
            ] 


class VfsRoot_Apps(vfs_node.Node):
    def children(self):
        return [
            vfs_fs.Directory(self, 'Apps', '/')
            ] 

 
