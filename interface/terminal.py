
from email.mime import text


class TerminalInterface:

    def __init__(self, engine, profile):
        self.engine = engine
        self.profile = profile

    def start(self):

        print("\n==============================")
        print("   STATISTICAL AUTOCOMPLETE")
        print("==============================")

        print("Type /exit to quit.\n")

        while True:

            text = input("You: ")

            if text.lower() == "/exit":
                print("Goodbye!")
                break

            # Learn from the user's input
            # Learn only completed words
            if text.endswith((" ", "\t")):

                completed_text = text

            else:

                words = text.split()

                completed_text = " ".join(words[:-1])

            if completed_text.strip():
                self.profile.learn(completed_text)

            # Generate suggestions
            suggestions = self.engine.suggest(text)

            # Rank suggestions
            suggestions = self.engine.rank_suggestions(
                suggestions
            )

            print("\nSuggestions:")

            if not suggestions:
                print("No suggestions available.")

            else:

                for index, (kind, word, score) in enumerate(
                    suggestions, start=1
                ):

                    print(
                        f"{index}. {word} "
                        f"[{kind}] ({score:.4f})"
                    )

            print()
