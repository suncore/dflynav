
import platform, os
from . import vfs_node, vfs_fs    

class VfsRoot(vfs_node.Node):
    def __init__(self):
        super(VfsRoot, self).__init__(None, '/')
    def children(self, async=True):
        return [vfs_fs.RootDirectory(self, 'Local', '/')] 


