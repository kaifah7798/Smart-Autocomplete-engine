
from pathlib import Path

from preprocessing.tokenizer import load_corpus
from models.ngram import NGramModel

from prediction.trie import Trie

from prediction.edit_distance import levenshtein_distance

from prediction.suggestion_engine import SuggestionEngine

# Locate dataset
dataset_path = Path(__file__).parent / "dataset" / "training.txt"


# Load dataset
sentences = load_corpus(dataset_path)


# Create and train model
model = NGramModel()
model.train(sentences)


# Bigram prediction
print("\nBIGRAM PREDICTIONS")

bigram_predictions = model.predict("love")

for word, probability in bigram_predictions:
    print(f"{word}: {probability:.2%}")


# Trigram prediction
print("\nTRIGRAM PREDICTIONS")

trigram_predictions = model.predict_trigram("i", "love")

for word, probability in trigram_predictions:
    print(f"{word}: {probability:.2%}")


# Test backoff


# Test 1: Trigram
context = ["i", "love"]

print("\nTEST 1: TRIGRAM")
print(model.predict_with_backoff(context))


# Test 2: Bigram fallback
context = ["unknown", "love"]

print("\nTEST 2: BIGRAM FALLBACK")
print(model.predict_with_backoff(context))


# Test 3: Unigram fallback
context = ["unknown"]

print("\nTEST 3: UNIGRAM FALLBACK")
print(model.predict_with_backoff(context))


print("\nSMOOTHED PREDICTIONS")

context = ["i", "love"]

predictions = model.predict_smoothed(context)

for word, probability in predictions:
    print(f"{word}: {probability:.2%}")


# Create Trie
trie = Trie()

# Insert all unique words from training data
for word in model.unigram_counts:
    trie.insert(word)

# Create unified suggestion engine
engine = SuggestionEngine(model, trie)

test_inputs = [
    "I love ",
    "I love pro",
    "I love pythn"
]

for user_input in test_inputs:

    print(f"\nINPUT: {user_input!r}")

    suggestions = engine.suggest(user_input)

    suggestions = engine.rank_suggestions(suggestions)

    for suggestion_type, word, score in suggestions:

     print(
        f"{suggestion_type}: {word} "
        f"(confidence: {score:.4f})"
     )

# Test word completion
prefix = "pro"

suggestions = trie.search_prefix(prefix)

# Rank suggestions by word frequency
suggestions.sort(
    key=lambda word: (-model.unigram_counts[word], word)
)

print("\nWORD COMPLETION")

for word in suggestions[:5]:
    print(f"{word}: {model.unigram_counts[word]}")


# Spelling correction

input_word = "pythn"

corrections = []

for word in model.unigram_counts:

    distance = levenshtein_distance(input_word, word)

    if distance <= 2:

        corrections.append(
            (word, distance, model.unigram_counts[word])
        )

# Sort by edit distance, then word frequency
corrections.sort(
    key=lambda item: (item[1], -item[2])
)

print("\nSPELLING CORRECTIONS")

for word, distance, frequency in corrections[:5]:

    print(
        f"{word}: distance={distance}, frequency={frequency}"
    )
