
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "dataset" / "raw"
OUTPUT_FILE = BASE_DIR / "dataset" / "training.txt"


def clean_book(text):

    # Remove Gutenberg header and footer when present
    text = re.sub(
        r"\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    text = re.sub(
        r"\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 2
    ]


def main():

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    files = list(RAW_DIR.rglob("*.txt"))

    if not files:
        print("No .txt files found inside dataset/raw")
        return

    all_sentences = []

    for file_path in files:

        print(f"Processing: {file_path.name}")

        text = file_path.read_text(
            encoding="utf-8-sig",
            errors="replace"
        )

        sentences = clean_book(text)
        all_sentences.extend(sentences)

        print(f"  Sentences: {len(sentences):,}")

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        for sentence in all_sentences:
            file.write(sentence + "\n")

    total_words = sum(
        len(sentence.split())
        for sentence in all_sentences
    )

    print("\nDATASET CREATED")
    print("----------------------------")
    print(f"Books processed: {len(files)}")
    print(f"Total sentences: {len(all_sentences):,}")
    print(f"Total words: {total_words:,}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
