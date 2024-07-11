import sys
import tkinter

from FifoTools import FifoTools
from SessionManager import SessionManager, SessionType

INPUT_PIPELINE_FILE = "presentation_json.cmd"
MESSAGE_SENTINEL = "@"
MESSAGE_QUIT = "QUIT"
MESSAGE_KILL = "KILL"
MESSAGE_NEWTERM = "TERM"
MESSAGE_NEWJSON = "JSON"



class PresentationJson:
    def __init__(self, root: tkinter.Tk):
        self.sessionManager = SessionManager(root)
        self.appDone = False
        self.pipe = None
        self.root = root

    @staticmethod
    def decodeMessage(msg) -> tuple[None, None] | tuple[str, str]:
        atPos = msg.find(MESSAGE_SENTINEL, 1)
        if atPos < 0:
            return None, None

        cmd = msg[1:atPos]
        body = msg[atPos + len(MESSAGE_SENTINEL):]

        return cmd, body

    def dispatch(self, msg: str) -> bool:
        cmd, body = self.decodeMessage(msg)

        if cmd == MESSAGE_QUIT:
            self.sessionManager.killAllSessions()
            self.appDone = True
        elif cmd == MESSAGE_KILL:
            self.sessionManager.killSession(body)
        elif cmd == MESSAGE_NEWTERM:
            if not self.sessionManager.newSession(body, SessionType.Terminal):
                print(f"Session creation failed, it probably exists {body}")
        elif cmd == MESSAGE_NEWJSON:
            if not self.sessionManager.newSession(body):
                print(f"Session creation failed, it probably exists {body}")
        else:
            self.sessionManager.sendTo(cmd, body)

        return not self.appDone

    def setup(self):
        if not FifoTools.createFifo(INPUT_PIPELINE_FILE):
            sys.exit(1)

        fname = FifoTools.getFifoPath(INPUT_PIPELINE_FILE)
        self.pipe = open(fname, "r")
        print(f"Listening on {FifoTools.getFifoPath(INPUT_PIPELINE_FILE)}")

    def shutdown(self):
        FifoTools.removeFifo(INPUT_PIPELINE_FILE)
        print("Done!")

    def process(self) -> bool:
        data = self.pipe.read()
        if len(data) == 0:
            return True

        data = data.strip()
        if data[0] == MESSAGE_SENTINEL:
            return self.dispatch(data)

        return True

