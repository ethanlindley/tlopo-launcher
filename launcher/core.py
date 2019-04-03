import os
import requests
import stat
import subprocess
import sys
import urllib

from typing import Tuple


class Core(object):

    def __init__(self, launcher):
        self.launcher = launcher

    def handleLogin(self, uname: str, pword: str) -> Tuple[str, bool]:
        # first, we'll try to login without 2fa, because at this point we don't know yet
        params = urllib.parse.urlencode({'username': uname,
                                        'password': pword})
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
        r = requests.post('https://api.tlopo.com/login/', data=params, headers=headers).json()
        return self.handleLoginResponse(r)

    def handleLogin2fa(self, uname: str, pword: str, gtoken) -> Tuple[str, bool]:
        # we're here because the user has 2fa enabled on their account
        params = urllib.parse.urlencode({'username': uname,
                                        'password': pword,
                                        'gtoken': gtoken})
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
        r = requests.post('https://api.tlopo.com/login/', data=params, headers=headers).json()
        return self.handleLoginResponse(r)

    def handleLoginResponse(self, resp: dict, uname: str='', pword: str='', gtoken: str='') -> Tuple[str, bool, str, str]:
        # let's see what the API has to say about the data we've fed it...
        status = resp['status']
        message = resp['message']

        if status == 7:
            # huzzah! we've made it through :D
            try:
                # if we needed the user's gtoken, let's cleanup that prompt
                self.launcher.gmgr.cleanup2fa()

                gameserver = resp['gameserver']
                token = resp['token']

                return message, True, gameserver, token
            except Exception as e:
                # 2fa wasn't needed in this case
                return message, True, gameserver, token
        elif status == 3:
            # looks like we need to perform some two-step authentication first -- let's get the user's gtoken
            self.launcher.gmgr.prompt2fa()
            return message, False, '', ''
        elif status == 1 or status == 4 or status == 5 or status == 8 or status == 9 or status == 10 or status == 11:
            # unable to connect :(
            return message, False, '', ''
        else:
            # any other case results in an error/status message
            return message, False, '', ''

    def launchProcess(self, gameserver: str, token: str) -> None:
        os.environ['TLOPO_GAMESERVER'] = gameserver
        os.environ['TLOPO_PLAYCOOKIE'] = token

        if sys.platform == 'linux' or sys.platform == 'linux2':
            # TODO - implement support for Linux-based systems
            pass
        elif sys.platform == 'darwin':
            # check if the shell script has proper permissions or not
            st = os.stat('./darwin/launch_client.sh')
            # checking for group execute permission
            if bool(st.st_mode & stat.S_IRWXU) is False:
                subprocess.run('chmod +x ./darwin/launch_client.sh')
            # execute the shell script
            subprocess.call('./darwin/launch_client.sh')
        elif sys.platform == 'win32':
            # TODO - implement support for Windows systems
            pass
