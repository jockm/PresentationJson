import tkinter
import tkinter as tk
from tkinter import scrolledtext, font as tkfont
import pyte
from pyte.streams import ByteStream
import time

def current_milli_time():
    return round(time.time() * 1000)
class TerminalWindow:
    def __init__(self, root: tk.Tk, title: str, cols=80, rows=25, fontSize=14,  inputCallback=None, echo=False):
        self.window = tkinter.Toplevel(root)
        self.window.title(title)

        # Terminal dimensions
        self.width = cols
        self.height = rows
        self.isEchoEnabled = echo
        self.inputCallback = inputCallback

        # Create a scrolled text widget to display the terminal output
        self.text_widget = scrolledtext.ScrolledText(self.window, wrap=tk.NONE, state="disabled")
        self.text_widget.pack(expand=True, fill=tk.BOTH)
        self.text_widget.bind("<Key>", self.on_key_press)

        # Initialize pyte screen and stream
        self.screen = pyte.Screen(cols, rows)
        self.stream = ByteStream(self.screen)

        # Attach screen to stream
        self.stream.attach(self.screen)

        # Dictionary to map pyte color names to Tkinter color names
        self.color_map = {
            "black": "black",
            "red": "red",
            "green": "green",
            "yellow": "yellow",
            "blue": "blue",
            "magenta": "magenta",
            "cyan": "cyan",
            "white": "white",
        }

        # Configure tags for different text attributes
        self.tag_config = {
            "default": {},  # Default tag configuration
            "bold": {"font": ("Courier", fontSize, "bold")},
            "italic": {"font": ("Courier", fontSize, "italic")},
            "underscore": {"underline": True},
        }

       # Add tags for each color defined in self.color_map
        for color_name, color_value in self.color_map.items():
            self.tag_config[f"fg_{color_name}"] = {"foreground": color_value}
            self.tag_config[f"bg_{color_name}"] = {"background": color_value}

    def addText(self, text):
        # Feed text (including VT100 escape sequences) to pyte stream
        self.stream.feed(text.encode("utf-8"))

    def on_key_press(self, event):
        theKey = event.char

        if self.inputCallback is not None:
            self.inputCallback(theKey)

        if self.isEchoEnabled:
            self.sendTextToTerminal(theKey)

    def destroy(self):
        self.window.destroy()

    def sendTextToTerminal(self, text):
        #todo need to scan for carriage returns and linefeeds and adjust the cursor position

        self.screen.cursor.y -= 1
        self.stream.feed(text.encode('utf-8'))
        self.screen.cursor.y += 1
        self.drawScreen()

    def drawScreen(self):
        self.text_widget.config(state="normal")

        # Clear existing tags
        self.text_widget.tag_delete("all")

        # Set initial display content
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, "\n".join(self.screen.display))

        # Draw the "cursor"
        self.text_widget.replace(f"{self.screen.cursor.y}.{self.screen.cursor.x}",
                                 f"{self.screen.cursor.y}.{self.screen.cursor.x + 1}",
                                 "_")

        for row in range(self.screen.lines):
            for col in range(self.screen.columns):
                # Check if row exists in buffer
                if row in self.screen.buffer:
                    row_data = self.screen.buffer[row]

                    # Check if col exists in row_data
                    if col in row_data:
                        buf_char = row_data[col]
                    else:
                        # Use default character attributes if col not in row_data
                        buf_char = self.screen.default_char
                else:
                    # Use default character attributes if row not in buffer
                    buf_char = self.screen.default_char

                fg_color = self.color_map.get(buf_char.fg, "black")
                bg_color = self.color_map.get(buf_char.bg, "white")
                bold = buf_char.bold
                italics = buf_char.italics
                underline = buf_char.underscore

                # Determine the tags to apply based on character attributes
                tags = []
                if bold:
                    tags.append("bold")
                if italics:
                    tags.append("italic")
                if underline:
                    tags.append("underscore")

                # Construct tag with foreground color and background color
                fg_tag = f"fg_{fg_color}"
                bg_tag = f"bg_{bg_color}"

                tags.append(fg_tag)
                tags.append(bg_tag)


                # Apply tags to the corresponding character
                for tag in tags:
                    self.text_widget.tag_add(tag, f"{row + 1}.{col}", f"{row + 1}.{col + 1}")

        # Configure tags for formatting
        for tag_name, config in self.tag_config.items():
            self.text_widget.tag_configure(tag_name, **config)

        self.text_widget.config(state="disabled")


# Example usage:
# if __name__ == "__main__":
#     term = TerminalWindow("VT100 Terminal Emulator", 80, 24)
#     term.addText("DUCK \x1b[31mHello, \x1b[1mWorld!\x1b[0mWORLD\n")  # Example: red text, bold "World!"
#     term.drawScreen()
#     term.run()
