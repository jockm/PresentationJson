import tkinter

from PresentationSession import PresentationSession
from SimpleTerminal import SimpleTerminal


class TerminalSession(PresentationSession):
	def __init__(self, root: tkinter.Tk, name: str):
		super().__init__(root, name)

		self.term = SimpleTerminal(root, name, cols=80, rows=25, echo=True, input_callback=self.userInput)

	# todo create the terminal window

	def kill(self):
		self.term.destroy()
		super(TerminalSession, self).kill()

	def receive(self, msg):
		self.term.sendTextToTerminal(msg)

	def userInput(self, msg):
		self.sendHome(msg)
