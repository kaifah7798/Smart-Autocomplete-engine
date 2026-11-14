
from collections import defaultdict, Counter
from multiprocessing import context


class NGramModel:

    def __init__(self):
        self.unigram_counts = Counter()
        self.bigram_counts = defaultdict(Counter)
        self.trigram_counts = defaultdict(Counter)

    def train(self, sentences):

        for sentence in sentences:

            # Unigram counts
            for word in sentence:
                self.unigram_counts[word] += 1

            # Bigram counts
            for i in range(len(sentence) - 1):

                current_word = sentence[i]
                next_word = sentence[i + 1]

                self.bigram_counts[current_word][next_word] += 1

            # Trigram counts
            for i in range(len(sentence) - 2):

                context = (sentence[i], sentence[i + 1])
                next_word = sentence[i + 2]

                self.trigram_counts[context][next_word] += 1

    def calculate_probabilities(self, predictions):

        if not predictions:
            return []

        total_count = sum(predictions.values())

        results = []

        for word, count in predictions.items():

            probability = count / total_count

            results.append((word, probability))

        results.sort(key=lambda item: item[1], reverse=True)

        return results[:5]

    def predict(self, word):

        predictions = self.bigram_counts.get(word, Counter())

        return self.calculate_probabilities(predictions)

    def predict_trigram(self, word1, word2):

        context = (word1, word2)

        predictions = self.trigram_counts.get(context, Counter())

        return self.calculate_probabilities(predictions)

    def predict_with_backoff(self, context):

        # Try trigram first
        if len(context) >= 2:

            trigram_context = tuple(context[-2:])

            predictions = self.trigram_counts.get(
                trigram_context, Counter()
            )

            if predictions:
                return self.calculate_probabilities(predictions)

        # Fall back to bigram
        if len(context) >= 1:

            last_word = context[-1]

            predictions = self.bigram_counts.get(
                last_word, Counter()
            )

            if predictions:
                return self.calculate_probabilities(predictions)

        # Fall back to unigram
        return self.calculate_probabilities(self.unigram_counts)

    
    def predict_smoothed(self, context):

     vocabulary_size = len(self.unigram_counts)

     # Try trigram
     if len(context) >= 2:

        trigram_context = tuple(context[-2:])

        predictions = self.trigram_counts.get(
            trigram_context, Counter()
        )

        if predictions:
            total_count = sum(predictions.values())

            results = []

            for word in self.unigram_counts:

                count = predictions.get(word, 0)

                probability = (
                    count + 1
                ) / (
                    total_count + vocabulary_size
                )

                results.append((word, probability))

            results.sort(key=lambda item: item[1], reverse=True)

            return results[:5]

     # Try bigram
     if len(context) >= 1:

        predictions = self.bigram_counts.get(
            context[-1], Counter()
        )

        if predictions:
            total_count = sum(predictions.values())

            results = []

            for word in self.unigram_counts:

                count = predictions.get(word, 0)

                probability = (
                    count + 1
                ) / (
                    total_count + vocabulary_size
                )

                results.append((word, probability))

            results.sort(key=lambda item: item[1], reverse=True)

            return results[:5]

     return self.calculate_probabilities(self.unigram_counts)

    