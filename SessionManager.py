import tkinter

from PresentationSession import PresentationSession
from enum import Enum

from TerminalSession import TerminalSession


class SessionType(Enum):
    Echo = 0
    Terminal = 1
    Json = 2


class SessionManager:
    def __init__(self, root: tkinter.Tk):
        self.sessions = {}
        self.root = root

    def newSession(self, name, sessiontype: SessionType = None) -> bool:
        if name in self.sessions:
            return False

        # newSession = None
        if sessiontype == SessionType.Echo:
            newSession = PresentationSession(self.root, name)
        elif sessiontype == SessionType.Terminal:
            newSession = TerminalSession(self.root, name)
        else:
            return False

        self.sessions[name] = newSession
        return True

    def killSession(self, name, delete=True):
        if name in self.sessions:
            self.sessions[name].kill()
            if delete:
                del self.sessions[name]

    def killAllSessions(self):
        for name in self.sessions:
            self.killSession(name, False)

        self.sessions.clear()

    def sendTo(self, name, body):
        if name in self.sessions:
            self.sessions[name].receive(body)
        pass
