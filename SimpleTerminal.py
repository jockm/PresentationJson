import tkinter
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyte
from pyte.streams import ByteStream

WINDOW_CLOSE_MESSAGE = "Are you sure? This may not terminate the process on the other side, and it may become "\
                       "unrecoverable"

KEYMAP = {
    "Escape": "",
    "Tab": "",
}


class SimpleTerminal:
    def __init__(self, root: tk.Tk, title: str, cols=80, rows=25, font_size=14, input_callback=None, echo=False):
        self.window = tkinter.Toplevel(root)
        self.window.title(title)

        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)

        # Terminal dimensions
        self.width = cols
        self.height = rows
        self.isEchoEnabled = echo
        self.inputCallback = input_callback

        # Create a scrolled text widget to display the terminal output
        self.scrolltext = scrolledtext.ScrolledText(self.window, wrap=tk.NONE, state="disabled")
        self.scrolltext.pack(expand=True, fill=tk.BOTH)
        self.window.bind("<Key>", self.onKey)

        # Initialize pyte screen and stream
        self.screen = pyte.Screen(cols, rows)
        self.stream = ByteStream(self.screen)

        # Attach screen to stream
        self.stream.attach(self.screen)

        # Yeah, this may seem silly now, but we may want to tweak these mappings later
        self.colorMapping = {
            "black": "black",
            "red": "red",
            "green": "green",
            "yellow": "yellow",
            "blue": "blue",
            "magenta": "magenta",
            "cyan": "cyan",
            "white": "white",
        }

        self.tag_config = {
            "default": {},  # TODO do we want to set a font here?
            "bold": {"font": ("Courier", font_size, "bold")},
            "italic": {"font": ("Courier", font_size, "italic")},
            "underscore": {"underline": True},
        }

        # Precalculate all the color mappings here now
        for name, value in self.colorMapping.items():
            self.tag_config[f"fg_{name}"] = {"foreground": value}
            self.tag_config[f"bg_{name}"] = {"background": value}

    def onClosing(self):
        if messagebox.askokcancel("Close Terminal?", WINDOW_CLOSE_MESSAGE):
            self.destroy()

    def clearScreen(self):
        self.stream.feed("\x1b[2J".encode('utf-8'))
        self.screen.cursor.x = 1
        self.screen.cursor.y = 1
        self.drawScreen()
        pass

    def onKey(self, event):
        print("duck", event.keysym)
        theKey = event.char

        # if theKey == '':
        #     match event.keysym:
        #         case

        if theKey is None:
            return

        if self.inputCallback is not None:
            self.inputCallback(theKey)

        if self.isEchoEnabled:
            self.sendTextToTerminal(theKey)

    def destroy(self):
        self.window.destroy()

    def sendTextToTerminal(self, text):
        # todo need to scan for carriage return and linefeed and adjust the cursor position
        # self.screen.cursor.y -= 1
        # self.screen.cursor.y += 1
        self.stream.feed(text.encode('utf-8'))
        self.drawScreen()

    def drawScreen(self):
        self.scrolltext.config(state="normal")

        # Clear existing tags
        self.scrolltext.tag_delete("all")

        # Set initial display content
        self.scrolltext.delete(1.0, tk.END)
        self.scrolltext.insert(tk.END, "\n".join(self.screen.display))

        # Draw the "cursor"
        self.scrolltext.replace(f"{self.screen.cursor.y + 1}.{self.screen.cursor.x}",
                                f"{self.screen.cursor.y + 1}.{self.screen.cursor.x + 1}",
                                "_")

        for row in range(self.screen.lines):
            if row not in self.screen.buffer:
                continue

            for col in range(self.screen.columns):
                row_data = self.screen.buffer[row]
                if col in row_data:
                    charAttributes = row_data[col]
                else:
                    charAttributes = self.screen.default_char

                fg_color = self.colorMapping.get(charAttributes.fg, "black")
                bg_color = self.colorMapping.get(charAttributes.bg, "white")

                bold = charAttributes.bold
                italics = charAttributes.italics
                underscore = charAttributes.underscore

                tagsToApply = []

                if bold:
                    tagsToApply.append("bold")

                if italics:
                    tagsToApply.append("italic")

                if underscore:
                    tagsToApply.append("underscore")

                tagsToApply.append(f"fg_{fg_color}")
                tagsToApply.append(f"bg_{bg_color}")

                for tag in tagsToApply:
                    self.scrolltext.tag_add(tag, f"{row + 1}.{col}", f"{row + 1}.{col + 1}")

        # TODO can we do this once up in the constructor?
        for tag_name, config in self.tag_config.items():
            self.scrolltext.tag_configure(tag_name, **config)

        self.scrolltext.config(state="disabled")


# Example usage:
# if __name__ == "__main__":
#     term = TerminalWindow("VT100 Terminal Emulator", 80, 24)
#     term.addText("DUCK \x1b[31mHello, \x1b[1mWorld!\x1b[0mWORLD\n")  # Example: red text, bold "World!"
#     term.drawScreen()
#     term.run()
