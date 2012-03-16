from PySide.QtCore import *
from PySide import QtGui
from utils import *
import Df

class Config():
    def __init__(self):
        self.settings = QSettings("ISS", "Dragonfly Navigator")
    
    def Load(self):
#        pos = self.settings.value("pos", QPoint(100, 100))
#        size = self.settings.value("size", QSize(400, 400))
#        Df.d.g.mw.resize(size)
#        Df.d.g.mw.move(pos)
        Df.d.bookmarks = self.settings.value("bookmarks", [ ])
        if type(Df.d.bookmarks) != type([]):
            Df.d.bookmarks = [ Df.d.bookmarks ]
        
    def Save(self):
        # save d.bookmarks as part of config file
#        self.settings.setValue("pos", Df.d.g.mw.pos())
#        self.settings.setValue("size", Df.d.g.mw.size())
        self.settings.setValue("bookmarks", Df.d.bookmarks)
