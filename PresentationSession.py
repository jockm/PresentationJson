import os
import tkinter

from FifoTools import FifoTools


class PresentationSession:
    def __init__(self, root: tkinter.Tk, name: str):
        self.sessionName = name

        if not FifoTools.createFifo(name):
            raise Exception("Failed to create fifo")

        self.returnPipeline = open(FifoTools.getFifoPath(name), "w")

    def kill(self):
        self.returnPipeline.close()
        FifoTools.removeFifo(self.sessionName)

    def receive(self, msg):
        # TODO write me, but in the meantime, just send it back
        self.sendHome(msg)

    def sendHome(self, msg):
        self.returnPipeline.write(f"@{self.sessionName}@{msg}")
        self.returnPipeline.flush()
