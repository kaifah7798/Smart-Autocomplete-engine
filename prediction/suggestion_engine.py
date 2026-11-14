
from preprocessing.tokenizer import tokenize
from prediction.edit_distance import levenshtein_distance


class SuggestionEngine:

    def __init__(self, model, trie):
        self.model = model
        self.trie = trie

    def suggest(self, text, limit=5):

        # Case 1: User has finished typing a word
        if text.endswith((" ", "\t", "\n")):

            context = tokenize(text)

            predictions = self.model.predict_with_backoff(context)

            return [
                ("next_word", word, probability)
                for word, probability in predictions[:limit]
            ]

        words = tokenize(text)

        if not words:
            return []

        current_word = words[-1]

        # Case 2: Exact word already exists
        if current_word in self.model.unigram_counts:

            predictions = self.model.predict_with_backoff(words)

            return [
                ("next_word", word, probability)
                for word, probability in predictions[:limit]
            ]

        # Case 3: Word completion
        completions = self.trie.search_prefix(current_word)

        completions = [
            word for word in completions
            if word != current_word
        ]

        if completions:

            completions.sort(
                key=lambda word: (
                    -self.model.unigram_counts[word],
                    word
                )
            )

            return [
                ("completion", word, self.model.unigram_counts[word])
                for word in completions[:limit]
            ]

        # Case 4: Spelling correction
        corrections = []

        for word in self.model.unigram_counts:

            distance = levenshtein_distance(current_word, word)

            if 0 < distance <= 2:

                corrections.append(
                    (word, distance, self.model.unigram_counts[word])
                )

        corrections.sort(
            key=lambda item: (item[1], -item[2], item[0])
        )

        return [
            ("correction", word, distance)
            for word, distance, frequency in corrections[:limit]
        ]
