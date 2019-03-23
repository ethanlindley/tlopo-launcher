import requests 
import urllib
import time


class LauncherBase(object):

    def __init__(self, launcher):
        self.launcher = launcher

    def getGtoken(self):
        return self.launcher.gui_mgr.objects['2fa_entry'].get()

    def handleLogin(self, uname, pword):
        # first, we'll try to login without 2fa
        params = urllib.parse.urlencode({'username': uname,
                                        'password': pword})
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
        r = requests.post('https://api.tlopo.com/login/', data=params, headers=headers).json()
        # note - we provide the username and password in case 2fa is needed to login further
        return self.handleLoginResponse(r)

    def handleLogin2fa(self, uname, pword, gtoken):
        # we're here because the user has 2fa enabled on their account
        gtoken = self.getGtoken()
        params = urllib.parse.urlencode({'username': uname,
                                        'password': pword,
                                        'gtoken': gtoken})
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
        r = requests.post('https://api.tlopo.com/login/', data=params, headers=headers).json()
        return self.handleLoginResponse(r)

    def handleLoginResponse(self, resp, uname='', pword='', gtoken=''):
        status = resp['status']
        message = resp['message']

        if status == 3:
            self.launcher.gui_mgr.prompt2fa()
            return None, None
        elif status == 1 or status == 4 or status == 5 or status == 8 or status == 9 or status == 10 or status == 11:
            return message, False
        elif status == 7:
            try:
                self.launcher.gui_mgr.cleanup2fa()
                return message, True
            except Exception as e:
                # 2fa wasn't needed in this case
                return message, True
        else:
            return message, False
