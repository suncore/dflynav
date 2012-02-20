
from . import vfs_node, vfs_fs, vfs_root, vfs_apps
import platform
if platform.system() == 'Windows':
    from . import vfs_fsNotify_Windows
else:
    from . import vfs_fsNotify_Linux
    
