from tkinter import *
from chat import get_response, bot_name

BG_COLOR = "#5e72e4"  # Blue
TEXT_COLOR = "#ffffff"  # White
FONT = "Helvetica 12"
FONT_BOLD = "Helvetica 12 bold"
MAUVE_COLOR = "#DABEBB"  # Rich Mauve

class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chatbot")
        self.window.geometry("470x550")
        self.window.configure(bg=BG_COLOR)

        # Head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Chatbot", font=FONT_BOLD, pady=10)
        head_label.pack(fill="x")

        # Tiny divider
        line = Label(self.window, width=450, bg=TEXT_COLOR)
        line.pack(fill="x")

        # Text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.pack(fill="both", expand=True)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # Scrollbar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.pack(side="right", fill="y")
        scrollbar.configure(command=self.text_widget.yview)

        # Bottom label
        bottom_label = Label(self.window, bg=BG_COLOR, height=80)
        bottom_label.pack(fill="x")

        # Message entry box
        self.msg_entry = Entry(bottom_label, bg="#ffffff", fg=BG_COLOR, font=FONT)
        self.msg_entry.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # Send button with rich mauve background
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=MAUVE_COLOR, command=lambda: self._on_enter_pressed(None))
        send_button.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

if __name__ == "__main__":
    app = ChatApplication()
    app.run()
