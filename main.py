from launcher.launcher import Launcher

try:
    app = Launcher()
    app.run()
except Exception as e:
    print(e)
