"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code
from main import SentenceEncoder, SentencePreprocessor


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

    #mark6

    preprocessor = SentencePreprocessor(stop_words, ())
    sentences = preprocessor.get_sentences(text)

    encoder = SentenceEncoder()
    encoder.encode_sentences(sentences)

    for sentence in sentences[:5]:
        print(f"Sentence id{sentence.get_position()}:")
        print(f"  Text: {sentence.get_text()}")
        print(f"  Tokens: {sentence.get_preprocessed()}")
        print(f"  id: {sentence.get_encoded()}")

    # result = None
    # assert result


if __name__ == "__main__":
    main()
