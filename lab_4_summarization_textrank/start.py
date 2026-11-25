"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code
from lab_4_summarization_textrank.main import (
    SentenceEncoder,
    SentencePreprocessor,
)


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "lab_4_summarization_textrank/assets/article_701.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()
    with open(
        "lab_4_summarization_textrank/assets/stop_words.txt", "r", encoding="utf-8"
    ) as text_file:
        stop_words = tuple(text_file.read().split("\n"))
    result = None

    # mark 6
    preprocessor = SentencePreprocessor(stop_words, punctuation=tuple(".,!?;:()[]{}\"'"))
    sentences = preprocessor.get_sentences(text)
    encoder = SentenceEncoder()
    encoder.encode_sentences(sentences)
    print(f"Encoded sentences: {sentences}")
    print(f"Encoder: {encoder}")
    print(f"Vocabulary size: {len(encoder._word2id)}")
    assert encoder


if __name__ == "__main__":
    main()
