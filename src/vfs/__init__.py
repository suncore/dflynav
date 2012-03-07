
from . import vfs_node, vfs_fs, vfs_root, vfs_apps, vfs_asyncJobs
import platform
if platform.system() == 'Windows':
    from vfs_fsNotify_Windows import *
else:
    from vfs_fsNotify_Linux import *
    
