from panda3d.core import *
from direct.showbase.Loader import *
from direct.gui.DirectGui import *


class GuiManager(object):

    def __init__(self, parent):
        self.parent = parent

        base.setBackgroundColor(255, 255, 255, 255)

        # keep track of GUI objects we have instantiated that we might need to access later
        self.objects = dict()
        
        # store the user's values without having them overwritten
        self._uname = ''
        self._pword = ''
        self._gtoken = ''

    def getUname(self):
        return self._uname

    def getPword(self):
        return self._pword

    def getGtoken(self):
        return self._gtoken

    def build(self):
        self.prepareWindow()

    def prepareWindow(self):
        # create the background
        cm = CardMaker('background')
        img = loader.loadTexture('etc/resources/images/bg.jpg')
        card = render2d.attachNewNode(cm.generate())
        card.setTransparency(TransparencyAttrib.MAlpha)
        card.setTexture(img)
        card.setPos(-1, 0, -1)
        card.setScale(2)

        # create our login objects
        uname_text = OnscreenText(
            text='Username',
            pos=(-0.6, 0.05), 
            scale=0.08,
            fg=(255, 255, 255, 255)
        )
        self.objects['uname_text'] = uname_text

        pword_text = OnscreenText(
            text='Password',
            pos=(-0.6, -0.2),
            scale=0.08,
            fg=(255, 255, 255, 255)
        )
        self.objects['pword_text'] = pword_text

        uname_entry = DirectEntry(
            text='', 
            scale=0.08, 
            initialText='',
            pos=(-0.35, 0, 0.04),
            image_color=(255,255,255,255)
        )
        self.objects['uname_entry'] = uname_entry
        uname_entry['focus'] = 1  # make the login entry box our default focus

        pword_entry = DirectEntry(
            text='', 
            scale=0.08, 
            initialText='',
            obscured=1,
            pos=(-0.35, 0, -0.21),
            image_color=(255, 255, 255, 255)
        )
        self.objects['pword_entry'] = pword_entry

        play_btn = DirectButton(
            text='Play',
            pos=(0.035, 0, -0.391),
            scale=0.09,
            command=self.prepareLogin,
            rolloverSound=loader.loadSfx('etc/resources/audio/btn_rollover.wav'),
            clickSound=loader.loadSfx('etc/resources/audio/btn_click.wav')
        )
        self.objects['play_btn'] = play_btn

        status_text = OnscreenText(
            text='',
            pos=(0.065, 0.21),
            scale=0.08,
            fg=(255, 255, 255, 255),
            align=TextNode.ACenter
        )
        self.objects['status_text'] = status_text

    def prompt2fa(self):
        # we need the user's 2fa token in order to login -- let's kindly ask them for it :)
        text = OnscreenText(
            text='Please enter your two-step authentication code here',
            pos=(0.68, 0.85),
            scale=0.06,
            fg=(255, 255, 255, 255)
        )
        self.objects['2fa_text'] = text

        entry = DirectEntry(
            text='',
            scale=0.08,
            initialText='',
            pos=(0.2895, 0, 0.65),
        )
        self.objects['2fa_entry'] = entry

        btn = DirectButton(
            text='Submit',
            pos=(0.691, 0, 0.45),
            scale=0.08,
            command=self.prepareLogin,
            rolloverSound=loader.loadSfx('etc/resources/audio/btn_rollover.wav'),
            clickSound=loader.loadSfx('etc/resources/audio/btn_click.wav')
        )
        self.objects['2fa_btn'] = btn

    def prepareLogin(self):
        if self.objects['uname_entry'].get() != '':
            self._uname = self.objects['uname_entry'].get()
        if self.objects['pword_entry'].get() != '':
            self._pword = self.objects['pword_entry'].get()
        try:
            # if the user is 2fa, let's get their gtoken
            if self.objects['2fa_entry'].get() != '':
                self._gtoken = self.objects['2fa_entry'].get()
        except:
            pass
        self.parent.beginLogin()

    def cleanup2fa(self):
        # cleanup 2fa prompt
        self.objects['2fa_text'].destroy()
        self.objects['2fa_entry'].destroy()
        self.objects['2fa_btn'].destroy()
        # quit keeping track of destroyed objects
        self.objects.pop('2fa_text')
        self.objects.pop('2fa_entry')
        self.objects.pop('2fa_btn')

    def updateStatus(self, response):
        self.objects['status_text'].setText(response)

    def cycleEntry(self):
        uname_entry = self.objects['uname_entry']
        pword_entry = self.objects['pword_entry']

        # if the username entry field is not "selected"
        if uname_entry['focus'] == 0:
            # put the username entry field in focus and the password entry field out of focus
            uname_entry['focus'] = 1
            pword_entry['focus'] = 0
        # if the password entry field is not "selected"
        elif pword_entry['focus'] == 0:
            pword_entry['focus'] = 1
            uname_entry['focus'] = 0
