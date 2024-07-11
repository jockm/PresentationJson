from PresentationJson import PresentationJson
from AppUI import appAnnounce, appSetup, appGiveTimeToUI

keepRunning = True


def mainLoop(root):
    global keepRunning

    app = PresentationJson(root)
    app.setup()

    appAnnounce()

    while keepRunning:
        appGiveTimeToUI()
        keepRunning = app.process()

    app.shutdown()
    root.destroy()


if __name__ == '__main__':
    root = appSetup()
    mainLoop(root)
