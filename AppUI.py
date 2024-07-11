import tkinter as tk
from tkinter import messagebox

import time

root: tk.Tk
label: tk.Label


def currentMillis():
    return round(time.time() * 1000)


def onClosing():
    global keepRunning
    if messagebox.askokcancel("Quit?", "Quitting will terminate all sessions with clients.  Are you sure?"):
        keepRunning = False


def appGiveTimeToUI(runForMillis: int = 50):
    global root

    stopTime = currentMillis() + runForMillis
    while currentMillis() < stopTime:
        root.update_idletasks()
        root.update()


def appAnnounce(msg: str = "PresentationJson is running."):
    global label
    label.config(text=msg)
    appGiveTimeToUI()


def appSetup():
    global keepRunning
    global root
    global label

    # Create a main windows with *something* in it.
    root = tk.Tk()
    root.title("PresentationJson")

    label = tk.Label(root, text="Waiting for client to connect...")
    label.pack(pady=20)

    # Capture when it is done
    root.protocol("WM_DELETE_WINDOW", onClosing)

    appGiveTimeToUI()
    return root


