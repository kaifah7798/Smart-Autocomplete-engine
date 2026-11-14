
from pathlib import Path
from preprocessing.tokenizer import load_corpus

# Locate the dataset
dataset_path = (
    Path(__file__).parent / "dataset" / "training.txt"
)

# Load and preprocess text
sentences = load_corpus(dataset_path)

# Display results
for sentence in sentences:
    print(sentence)
