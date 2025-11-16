import tkinter as tk
import random
from menu_concept import menu
from gemini_api import *

class MorseTerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='black')
        self.blink = True
        self.current_morse = ""
        self.final_message_words = []
        self.menu_system = menu(WORDS_DICT)

        self.showing_help = False
        self.art_animating = False
        self.current_art_line = 0

        self.game_mode = False
        self.game_target_word = ""
        self.game_hints = []
        self.hint_index = 0
        self.game_score = 0
        self.game_streak = 0
        self.game_attempts = 0
        self.max_attempts = 5

        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(root, bg="black")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.path_label = tk.Label(self.left_frame, text="root", font=("Courier", 24),
                                   fg="lime", bg="black", anchor="w")
        self.path_label.pack(fill="x", padx=5, pady=5)
        self.options_display = tk.Text(self.left_frame, width=50, font=("Courier", 28),
                                       bg="black", fg="lime", insertbackground="lime",
                                       borderwidth=0, highlightthickness=0)
        self.options_display.config(state=tk.DISABLED)
        self.options_display.pack(fill="both", expand=True, padx=5, pady=5)

        self.right_frame = tk.Frame(root, bg="black")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.game_display = tk.Text(self.right_frame, width=40, font=("Courier", 24),
                                    bg="black", fg="cyan", insertbackground="cyan",
                                    borderwidth=0, highlightthickness=0)
        self.game_display.config(state=tk.DISABLED)
        self.game_display.pack(fill="both", expand=True, padx=5, pady=5)

        self.bottom_frame = tk.Frame(root, bg="black")
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.final_label = tk.Label(self.bottom_frame, text="> ", font=("Courier", 24),
                                    fg="lime", bg="black", anchor="w")
        self.final_label.pack(fill="x")
        self.interpreted_label = tk.Label(self.bottom_frame, text="", font=("Courier", 24),
                                          fg="cyan", bg="black", anchor="w", justify="left",
                                          wraplength=root.winfo_screenwidth() - 40)
        self.interpreted_label.pack(fill="x", pady=(2, 2))
        self.morse_label = tk.Label(self.bottom_frame, text=">", font=("Courier", 30),
                                    fg="cyan", bg="black", anchor="w")
        self.morse_label.pack(fill="x")

        root.bind(".", lambda e: self.add_symbol("."))
        root.bind("-", lambda e: self.add_symbol("-"))
        root.bind("<Return>", lambda e: self.submit_morse())
        root.bind("<BackSpace>", lambda e: self.backspace_morse())
        root.bind("<Configure>", lambda e: self.interpreted_label.config(wraplength=e.width - 40))

        self.blink_cursor()
        self.update_display()

    def start_game(self):
        self.game_mode = True
        self.game_target_word = self.pick_random_word()
        self.game_hints = self.get_progressive_hints(self.game_target_word)
        self.hint_index = 0
        self.game_attempts = 0
        self.update_game_display()
        self.interpreted_label.config(text="game on! select word and submit with -....")

    def pick_random_word(self):
        def collect_words(node):
            results = []
            if isinstance(node, list):
                return node
            if isinstance(node, dict):
                for v in node.values():
                    results.extend(collect_words(v))
            return results
        all_words = collect_words(WORDS_DICT)
        return random.choice(all_words).strip().lower()

    def get_progressive_hints(self, word):
        try:
            hints = get_gemini_hint(word)
            if len(hints) < 3:
                hints += [f"the word has {len(word)} letters."] * (3 - len(hints))
        except Exception:
            hints = [
                f"the word starts with '{word[0].upper()}'.",
                f"the word has {len(word)} letters.",
                f"word: {word.upper()}."
            ]
        return hints

    def update_game_display(self):
        self.game_display.config(state=tk.NORMAL)
        self.game_display.delete(1.0, tk.END)
        if self.game_mode:
            self.game_display.insert(
                tk.END,
                f"WORD GAME\nscore: {self.game_score} | streak: {self.game_streak} | attempt: {self.game_attempts}/{self.max_attempts}\n\n"
                f"hint #{self.hint_index + 1}: {self.game_hints[self.hint_index]}\n"
            )
        self.game_display.config(state=tk.DISABLED)

    def add_symbol(self, symbol):
        if not self.art_animating:
            self.current_morse += symbol
            self.update_morse_label()

    def backspace_morse(self):
        if not self.art_animating:
            self.current_morse = self.current_morse[:-1]
            self.update_morse_label()

    def update_morse_label(self):
        cursor = "_" if self.blink else ""
        self.morse_label.config(text=f">{self.current_morse}{cursor}")

    def blink_cursor(self):
        self.blink = not self.blink
        self.update_morse_label()
        self.root.after(500, self.blink_cursor)

    def submit_morse(self):
        if self.art_animating:
            return
        choice = self.current_morse
        self.current_morse = ""
        self.update_morse_label()
        root_level = (self.menu_system.path == [])

        if root_level and choice == ".--.":
            self.start_game()
            return
        if self.game_mode and choice == "-.-.-":
            self.game_mode = False
            self.game_target_word = ""
            self.game_hints = []
            self.hint_index = 0
            self.game_attempts = 0
            self.game_display.config(state=tk.NORMAL)
            self.game_display.delete(1.0, tk.END)
            self.game_display.config(state=tk.DISABLED)
            self.interpreted_label.config(text="exited game")
            self.update_display()
            return

        if self.game_mode and choice == "-....":
            if not self.final_message_words:
                self.interpreted_label.config(text="no word selected yet")
                return
            guess = self.final_message_words[-1].lower()
            self.game_attempts += 1
            if guess == self.game_target_word:
                self.game_score += 1 + self.game_streak
                self.game_streak += 1
                self.interpreted_label.config(
                    text=f"correct! word: {self.game_target_word.upper()}\nScore: {self.game_score} | streak: {self.game_streak}"
                )
                self.start_game()
            else:
                if self.game_attempts >= self.max_attempts:
                    self.interpreted_label.config(
                        text=f"incorrect, word: {self.game_target_word.upper()}\nScore: {self.game_score} | streak reset"
                    )
                    self.game_streak = 0
                    self.start_game()
                else:
                    self.hint_index = min(self.hint_index + 1, len(self.game_hints) - 1)
                    self.interpreted_label.config(
                        text=f"incorrect, your guess: {guess.upper()}\nhint #{self.hint_index + 1}: {self.game_hints[self.hint_index]}"
                    )
                    self.update_game_display()
            return

        if root_level:
            if choice == "-.-":
                self.animate_ascii(self.cat_art())
                return
            elif choice == "-.-.-.-":
                self.animate_ascii(self.trippy_art(), speed=90, repeat=3)
                return
            elif choice == "---...---":
                self.animate_ascii(self.hackrpi_art())
                return

        if choice == '...---...':
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
            return
        else:
            try:
                num_str = commands[choice]
                idx = int(num_str) - 1
                current_options = self.menu_system.options()
                if self.menu_system.on_leaf():
                    if 0 <= idx < len(current_options):
                        self.final_message_words.append(current_options[idx])
                        self.menu_system.current_position = self.menu_system.file_system
                        self.menu_system.path = []
                else:
                    if 0 <= idx < len(current_options):
                        self.menu_system.move_forward(current_options[idx])
            except:
                pass

        self.update_display()

    def show_help(self):
        self.interpreted_label.config(text="""
commands:
....   move back
.....  return to root
...... interpret message / submit word for game
.--.   start game
-.-.-  exit game
""")

    def update_display(self):
        if self.art_animating:
            return
        path_str = "root" + (" > " + " > ".join(self.menu_system.path) if self.menu_system.path else "")
        if self.game_mode:
            path_str += "  GAME ACTIVE"
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

        if self.game_mode:
            self.update_game_display()

    def animate_ascii(self, art_lines, speed=140, repeat=1, end_delay=900):
        self.art_animating = True
        self.current_art_line = 0
        frames = art_lines * repeat
        self.options_display.config(state=tk.NORMAL)
        self.options_display.delete(1.0, tk.END)
        def draw():
            if self.current_art_line < len(frames):
                self.options_display.insert(tk.END, frames[self.current_art_line] + "\n")
                self.options_display.see(tk.END)
                self.current_art_line += 1
                self.root.after(speed, draw)
            else:
                self.root.after(end_delay, finish)
        def finish():
            self.art_animating = False
            self.update_display()
        draw()

    def cat_art(self):
        return [
            "      /\\     /\\",
            "     {  `---'  }",
            "     {  O   O  }",
            "     ~~>  V  <~~",
            "      \\  \\|/  /",
            "       `-----'____",
            "       /     \\    \\_",
            "      {       }\\  )_\\_   _",
            "      |  \\_/  |/ /  \\_\\_/ )",
            "       \\__/  /(_/     \\__/",
            "         (__/"
        ]

    def trippy_art(self):
        return [
            " ~~~    *    ~~~    *    ~~~",
            " *    ~~~    *    ~~~    *  ",
            "~~~   *   ~~~   *   ~~~   * ",
            "  *    ~~~    *    ~~~    * ",
            "~~~    *    ~~~    *    ~~~ ",
            " *   ~~~   *   ~~~   *   ~~~",
        ]

    def hackrpi_art(self):

        return [
        "H   H AAAAA CCCCC K   K    RRRR  PPPP  I",
        "H   H A   A C     K  K     R   R P   P I",
        "HHHHH AAAAA C     KKK      RRRR  PPPP  I",
        "H   H A   A C     K  K     R R   P     I",
        "H   H A   A CCCCC K   K    R  R  P     I"
        ]



if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='black')
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    app = MorseTerminalApp(root)
    root.mainloop()
