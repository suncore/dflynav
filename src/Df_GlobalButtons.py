
import Df


helptext = '''
Welcome to Dragonfly Navigator!

These are some tips of not-so-obvious features in this program:

Viewing folders: Press the right mouse button on a folder to open it. (Double-click left mouse button also works.)

Opening files: Press the right mouse button on a file to open it. (Double-click left mouse button also works.)

Copying files: Select files on one side and press the copy button. The files will be copied to the opposite side/folder. Other operations work the same way. Selected files/folders are the source and the destination is the opposite folder. Some operations, like delete, only affects the selected files, not the opposite folder.

Creating a folder: Type the name of the folder in the folder entry. If it does not exist, you will be asked if you want it created.

If you have opened or copied files, the list at the bottom shows a history of operations. Click on one to see more details.

It is possible to preview picture files. Move the mouse cursor over a picture file and press the Alt button. A preview of the picture file will be shown on the opposite side. In the same manner, it is also possible to quick-browse folders by moving the mouse cursor over a folder and pressing the Alt button.

The rest should be self-explanatory. If not, drop me a mail at info@dflynav.com.
'''


class GlobalButtons(object):
    def __init__(self, mw, configW, helpW):
        mw.refresh.clicked.connect(self.refresh)
        mw.configure.clicked.connect(self.configure)
        mw.help.clicked.connect(self.help)
        self.configW = configW
        self.helpW = helpW
        self.helpW.helpText.setPlainText(helptext)
        
    def refresh(self):
        Df.d.lp.setPath(Df.d.lp.cd)
        Df.d.rp.setPath(Df.d.rp.cd)

    def configure(self):
        self.configW.show()
        
    def help(self):
        self.helpW.show()
        