
from . import vfs_node, vfs_fs, vfs_root, vfs_asyncJobs
import platform
if platform.system() == 'Windows':
    from vfs_fsNotify_Windows import *
    from . import vfs_apps_Windows
else:
    from vfs_fsNotify_Linux import *
    
