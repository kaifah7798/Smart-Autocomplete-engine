
import re


def tokenize(text):
    text = text.lower()
    words = re.findall(r"[a-z]+(?:'[a-z]+)?", text)
    return words


def load_corpus(file_path):

    sentences = []

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            words = tokenize(line)

            if words:
                sentences.append(words)

    return sentences
