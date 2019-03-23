import requests 
import urllib


class Core(object):

    def __init__(self, launcher):
        self.launcher = launcher

    def handleLogin(self, uname, pword):
        # first, we'll try to login without 2fa, because at this point we don't know yet
        params = urllib.parse.urlencode({'username': uname,
                                        'password': pword})
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
        r = requests.post('https://api.tlopo.com/login/', data=params, headers=headers).json()
        return self.handleLoginResponse(r)

    def handleLogin2fa(self, uname, pword, gtoken):
        # we're here because the user has 2fa enabled on their account
        params = urllib.parse.urlencode({'username': uname,
                                        'password': pword,
                                        'gtoken': gtoken})
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
        r = requests.post('https://api.tlopo.com/login/', data=params, headers=headers).json()
        return self.handleLoginResponse(r)

    def handleLoginResponse(self, resp, uname='', pword='', gtoken=''):
        # let's see what the API has to say about the data we've fed it...
        status = resp['status']
        message = resp['message']

        if status == 3:
            # looks like we need to perform some two-step authentication first -- let's get the user's gtoken
            self.launcher.gmgr.prompt2fa()
            return None, None
        elif status == 1 or status == 4 or status == 5 or status == 8 or status == 9 or status == 10 or status == 11:
            # unable to connect :(
            return message, False
        elif status == 7:
            # huzzah! we've made it through :D
            try:
                self.launcher.gmgr.cleanup2fa()
                return message, True
            except Exception as e:
                # 2fa wasn't needed in this case
                return message, True
        else:
            # we don't handle any other case outside of the above conditionals
            return message, False
