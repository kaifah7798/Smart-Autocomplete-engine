
import os
import platform

class TerminalInterface:

    RESET = "\033[0m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"

    def __init__(self, engine, profile):
        self.engine = engine
        self.profile = profile

    def clear_screen(self):
        os.system("cls" if platform.system() == "Windows" else "clear")

    def banner(self):

        print(self.CYAN + self.BOLD)
        print("======================================================")
        print("             SMART AUTOCOMPLETE ENGINE")
        print("======================================================")
        print(self.RESET)

        print(self.GRAY + "  Statistical Language Model | N-Gram | Trie")
        print("  Spelling Correction | Personalization")
        print(self.RESET)

        print(self.GREEN + "  SYSTEM STATUS: ONLINE" + self.RESET)
        print("  Type text to receive suggestions.")
        print("  Type /help to see available commands.")
        print("------------------------------------------------------")

    def show_help(self):

        print("\n" + self.CYAN + "AVAILABLE COMMANDS" + self.RESET)
        print("  /help     - Show commands")
        print("  /profile  - View your learned vocabulary")
        print("  /clear    - Clear terminal")
        print("  /exit     - Exit application")

    def show_profile(self):

        print("\n" + self.CYAN + "USER PROFILE" + self.RESET)
        print("--------------------------------------")

        if not self.profile.word_counts:
            print("No personal vocabulary learned yet.")
            return

        sorted_words = self.profile.word_counts.most_common(15)

        for word, count in sorted_words:
            print(f"  {word:<20} {count:>5}")

        print("--------------------------------------")
        print(f"Total unique words: {len(self.profile.word_counts)}")

    def learn_completed_words(self, text):

        if text.endswith((" ", "\t", "\n")):
            completed_text = text
        else:
            words = text.split()
            completed_text = " ".join(words[:-1])

        if completed_text.strip():
            self.profile.learn(completed_text)

    def show_suggestions(self, suggestions):

        print("\n" + self.CYAN + "  AUTOCOMPLETE SUGGESTIONS" + self.RESET)
        print("  ------------------------------------------------")

        if not suggestions:
            print(self.YELLOW + "  No suggestions available." + self.RESET)
            print("  ------------------------------------------------")
            return

        print(
            self.GRAY +
            f"  {'NO.':<5}{'SUGGESTION':<22}{'TYPE':<15}{'SCORE':>9}"
            + self.RESET
        )

        print("  ------------------------------------------------")

        for index, (kind, word, score) in enumerate(suggestions, 1):

            if kind == "next_word":
                color = self.GREEN
                label = "PREDICTION"

            elif kind == "completion":
                color = self.CYAN
                label = "COMPLETION"

            else:
                color = self.YELLOW
                label = "CORRECTION"

            print(
                color +
                f"  {index:<5}{word:<22}{label:<15}{score:>9.4f}"
                + self.RESET
            )

        print("  ------------------------------------------------")

    def start(self):

        self.banner()

        while True:

            try:
                text = input(
                    self.BOLD + self.WHITE + "\n  YOU > " + self.RESET
                )

            except (KeyboardInterrupt, EOFError):
                print("\n\n  Application closed.")
                break

            command = text.strip().lower()

            if command in ("/exit", "exit"):
                print(self.GREEN + "\n  Thank you for using Smart Autocomplete!")
                print("  Goodbye!\n" + self.RESET)
                break

            elif command == "/help":
                self.show_help()
                continue

            elif command == "/profile":
                self.show_profile()
                continue

            elif command == "/clear":
                self.clear_screen()
                self.banner()
                continue

            elif not text.strip():
                continue

            # Learn only completed words
            self.learn_completed_words(text)

            # Generate and rank suggestions
            suggestions = self.engine.suggest(text)
            suggestions = self.engine.rank_suggestions(suggestions)

            self.show_suggestions(suggestions)
