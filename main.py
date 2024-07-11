import tkinter as tk
from tkinter import messagebox

from PresentationJson import PresentationJson

keepRunning = True
root: tk.Tk


def onClosing():
    global keepRunning
    if messagebox.askokcancel("Quit?", "Quitting will terminate all sessions with clients.  Are you sure?"):
        keepRunning = False


def main():
    global keepRunning

    # Create a main windows with *something* in it.
    root = tk.Tk()
    root.title("PresentationJson")

    label = tk.Label(root, text="PresentationJson Running")
    label.pack(pady=20)

    # Capture when it is done
    root.protocol("WM_DELETE_WINDOW", onClosing)

    app = PresentationJson(root)
    app.setup()

    while keepRunning:
        root.update_idletasks()
        root.update()

        keepRunning = app.runOnce()

    app.shutdown()
    root.destroy()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
