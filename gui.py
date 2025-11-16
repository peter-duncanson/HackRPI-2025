import tkinter as tk
from menu_concept import menu
from gemini_api import interpret_morse_output, WORDS_DICT, commands, commands_mapping

class MorseTerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='black')
        self.blink = True
        self.current_morse = ""
        self.final_message_words = []
        self.menu_system = menu(WORDS_DICT)

        self.showing_interpretation = False
        self.showing_help = False  # NEW: separate flag for help

        # --- Path label (row 0) ---
        self.path_label = tk.Label(
            root, text="root", font=("Courier", 24),
            fg="lime", bg="black", anchor="w"
        )
        self.path_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # --- Options display (row 1) ---
        self.options_display = tk.Text(
            root, width=60, font=("Courier", 34),
            bg="black", fg="lime", insertbackground="lime",
            borderwidth=0, highlightthickness=0
        )
        self.options_display.config(state=tk.DISABLED)
        self.options_display.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # --- Bottom panel (row 2) ---
        self.bottom_frame = tk.Frame(root, bg="black")
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.final_label = tk.Label(
            self.bottom_frame, text="> ", font=("Courier", 24),
            fg="lime", bg="black", anchor="w"
        )
        self.final_label.pack(fill="x")

        self.interpreted_label = tk.Label(
            self.bottom_frame, text="", font=("Courier", 24),
            fg="cyan", bg="black", anchor="w", justify="left",
            wraplength=root.winfo_screenwidth() - 40
        )
        self.interpreted_label.pack(fill="x", pady=(2,2))

        self.morse_label = tk.Label(
            self.bottom_frame, text=">", font=("Courier", 30),
            fg="cyan", bg="black", anchor="w"
        )
        self.morse_label.pack(fill="x")

        # --- Grid weights to make options display expand ---
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # --- Key bindings ---
        root.bind(".", lambda e: self.add_symbol("."))
        root.bind("-", lambda e: self.add_symbol("-"))
        root.bind("<Return>", lambda e: self.submit_morse())

        root.bind("<Configure>", lambda e: self.interpreted_label.config(wraplength=e.width - 40))

        self.blink_cursor()
        self.update_display()

    # --- Morse input methods ---
    def add_symbol(self, symbol):
        self.current_morse += symbol
        self.update_morse_label()

    def backspace_morse(self):
        self.current_morse = self.current_morse[:-1]
        self.update_morse_label()

    def update_morse_label(self):
        cursor = "_" if self.blink else ""
        self.morse_label.config(text=f">{self.current_morse}{cursor}")

    def blink_cursor(self):
        self.blink = not self.blink
        self.update_morse_label()
        self.root.after(500, self.blink_cursor)

    # --- Menu logic ---
    def submit_morse(self):
        # --- EXIT HELP ---
        if self.showing_help:
            self.interpreted_label.config(text="")
            self.showing_help = False
            self.update_display()
            return

        # --- EXIT INTERPRETATION ---
        elif self.showing_interpretation:
            self.menu_system.current_position = self.menu_system.file_system
            self.menu_system.path = []
            self.final_message_words = []
            self.showing_interpretation = False
            self.update_display()
            return

        # --- PROCESS MORSE INPUT ---
        choice = self.current_morse
        self.current_morse = ""
        self.update_morse_label()
        current_options = self.menu_system.options()

        if choice == "...---...":
            self.show_help()
            return
        elif choice == "....": 
            self.menu_system.move_back()
        elif choice == ".....":  
            self.menu_system.current_position = self.menu_system.file_system
            self.menu_system.path = []
        elif choice == "......":  
            sentence = interpret_morse_output(self.final_message_words)
            if sentence:
                self.interpreted_label.config(text="\n" + sentence)
            self.showing_interpretation = True
            return
        else:
            try:
                num_str = commands[choice]
                idx = int(num_str) - 1
                if self.menu_system.on_leaf():
                    if 0 <= idx < len(current_options):
                        self.final_message_words.append(current_options[idx])
                        self.menu_system.current_position = self.menu_system.file_system
                        self.menu_system.path = []
                else:
                    if 0 <= idx < len(current_options):
                        self.menu_system.move_forward(current_options[idx])
            except (KeyError, ValueError):
                pass

        self.update_display()

    # --- Help interface ---
    def show_help(self):
        help_text = """
commands:
....      - move back
.....     - return to root
......    - interpret
"""
        self.interpreted_label.config(text=help_text)
        self.showing_help = True

    # --- Display update ---
    def update_display(self):
        path_str = "root" if not self.menu_system.path else "root > " + " > ".join(self.menu_system.path)
        self.path_label.config(text=path_str)

        current_options = self.menu_system.options()
        self.options_display.config(state=tk.NORMAL)
        self.options_display.delete(1.0, tk.END)

        morse_keys = [commands_mapping[i] for i in range(1, len(current_options)+1) if i in commands_mapping]
        max_len = max((len(k) for k in morse_keys), default=0)

        for i, option in enumerate(current_options, 1):
            if i in commands_mapping:
                key = commands_mapping[i].ljust(max_len)
                self.options_display.insert(tk.END, f"{key}  {option}\n")

        self.options_display.config(state=tk.DISABLED)
        self.final_label.config(text=" ".join(self.final_message_words))


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='black')
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    app = MorseTerminalApp(root)
    root.mainloop()