
import json
from collections import Counter
from pathlib import Path

from preprocessing.tokenizer import tokenize


class UserProfile:

    def __init__(self, file_path):

        self.file_path = Path(file_path)
        self.word_counts = Counter()

        self.load()

    def load(self):

        if self.file_path.exists():

            with open(self.file_path, "r", encoding="utf-8") as file:

                data = json.load(file)

                self.word_counts.update(data)

    def learn(self, text):

        words = tokenize(text)

        for word in words:
            self.word_counts[word] += 1

        self.save()

    def save(self):

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(self.file_path, "w", encoding="utf-8") as file:

            json.dump(
                dict(self.word_counts),
                file,
                indent=4
            )

    def get_frequency(self, word):

        return self.word_counts[word]
