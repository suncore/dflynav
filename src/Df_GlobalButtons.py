
import Df

class GlobalButtons(object):
    def __init__(self, mw, configW):
        mw.refresh.clicked.connect(self.refresh)
        mw.configure.clicked.connect(self.configure)
        self.configW = configW
        
    def refresh(self):
        Df.d.lp.setPath(Df.d.lp.cd)
        Df.d.rp.setPath(Df.d.rp.cd)

    def configure(self):
        self.configW.show()