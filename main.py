
from pathlib import Path

from preprocessing.tokenizer import load_corpus
from models.ngram import NGramModel

from prediction.trie import Trie
from prediction.suggestion_engine import SuggestionEngine
from prediction.user_profile import UserProfile

from interface.terminal import TerminalInterface


def main():

    base_path = Path(__file__).parent

    # Load training dataset
    dataset_path = base_path / "dataset" / "training.txt"
    sentences = load_corpus(dataset_path)

    if not sentences:
        print("Error: Training dataset is empty.")
        return

    # Train language model
    model = NGramModel()
    model.train(sentences)
   
    # Build Trie
    trie = Trie()

    for word in model.unigram_counts:
        trie.insert(word)

    # Load user profile
    profile_path = base_path / "dataset" / "user_profile.json"
    profile = UserProfile(profile_path)

    # Initialize suggestion engine
    engine = SuggestionEngine(
        model,
        trie,
        profile=profile,
        personalization_weight=0.3
    )

    # Launch application
    app = TerminalInterface(engine, profile)
    app.start()


if __name__ == "__main__":
    main()
