from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

from launcher import globals
from launcher.gui_mgr import GuiManager
from launcher.core import Core

# load our configuration file
loadPrcFile('etc/config.prc')


class Launcher(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)

        # instantiate some of our core classes -- we'll need to access these throughout the program
        self.gmgr = GuiManager(self)  # responsible for building the frontend objects
        self.core = Core(self)  # responsible for handling backend API tasks

        # begin building the frontend client application
        self.setup()

    def setup(self) -> None:
        # setup our GUI
        self.gmgr.build()
        
        base.accept('tab', self.gmgr.cycleEntry)

    def beginLogin(self) -> None:
        # let's grab our login information from the GUI manager
        uname = self.gmgr.getUname()
        pword = self.gmgr.getPword()
        gtoken = self.gmgr.getGtoken()

        # first, some basic sanity checking
        if uname == '':
            if pword == '':
                self.gmgr.updateStatus('{}'.format(globals.responses[12]))
            else:
                self.gmgr.updateStatus('{}'.format(globals.responses[13]))
        elif uname != '' and pword == '':
            self.gmgr.updateStatus('{}'.format(globals.responses[14]))
        else:
            # finally, we've passed all the tests and can begin authenticating with the API
            self.gmgr.updateStatus('Attempting to login...')

            if gtoken != '':
                # are we trying to perform 2fa authentication?
                message, logged_in = self.core.handleLogin2fa(uname, pword, gtoken)
            else:
                message, logged_in = self.core.handleLogin(uname, pword)

            # let's update the client and inform the user of whether they're successfully logged in or not
            if logged_in is False:
                self.gmgr.updateStatus('{}'.format(message))
            elif logged_in is True:
                self.gmgr.updateStatus('{}'.format(message))
                # TODO - now that we've logged in, let's start the client, assuming that the user's assets are up-to-date
                # side note - TLoPO, pls develop a public DL server API :|
