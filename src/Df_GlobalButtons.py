
import Df




class GlobalButtons(object):
    def __init__(self, mw, configW, helpW):
        mw.refresh.clicked.connect(self.refresh)
        mw.configure.clicked.connect(self.configure)
        mw.help.clicked.connect(self.help)
        self.configW = configW
        self.helpW = helpW
        #self.helpW.helpText.setText(helptext)
        
    def refresh(self):
        Df.d.lp.setPath(Df.d.lp.cd)
        Df.d.rp.setPath(Df.d.rp.cd)

    def configure(self):
        self.configW.show()
        
    def help(self):
        f = open("src/res/helptext.html")
        helptext = f.read()
        f.close()
        self.helpW.helpText.setHtml(helptext)
        self.helpW.show()
        