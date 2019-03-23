from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

from launcher import globals
from launcher.gui.gui_manager import GuiManager
from launcher.base.launcher_base import LauncherBase

# load our configuration file
loadPrcFile('etc/config.prc')


class Launcher(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)

        self.gui_mgr = GuiManager(self)
        self.launcher_base = LauncherBase(self)

        self.setup()

    def setup(self):
        # setup our GUI
        self.gui_mgr.build()
        
        base.accept('tab', self.gui_mgr.cycleEntry)

    def beginLogin(self, uname, pword, gtoken):
        if uname == '':
            if pword == '':
                self.gui_mgr.updateStatus('ERROR: {}'.format(globals.responses[12].lower()))
            else:
                self.gui_mgr.updateStatus('ERROR: {}'.format(globals.responses[13].lower()))
        elif uname != '' and pword == '':
            self.gui_mgr.updateStatus('ERROR: {}'.format(globals.responses[14].lower()))
        else:
            self.gui_mgr.updateStatus('Attempting to login...')

            if gtoken != '':
                message, logged_in = self.launcher_base.handleLogin2fa(uname, pword, gtoken)
            else:
                message, logged_in = self.launcher_base.handleLogin(uname, pword)

            # let's update the client and inform the user of whether they're successfully logged in or not
            if logged_in is False:
                self.gui_mgr.updateStatus('ERROR: {}'.format(message.lower()))
            elif logged_in is True:
                self.gui_mgr.updateStatus('{}'.format(message))
