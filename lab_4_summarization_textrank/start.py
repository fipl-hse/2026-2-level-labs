"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code

from lab_4_summarization_textrank.main import SentenceEncoder, SentencePreprocessor


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
    punctuation = (".", ",", "!", "?")
    sentence_preprocessor = SentencePreprocessor(stop_words, punctuation)
    sentences = sentence_preprocessor.get_sentences(text)
    sentence_encoder = SentenceEncoder()
    sentence_encoder.encode_sentences(sentences)
    result = tuple(sentence.get_encoded() for sentence in sentences)
    assert result


if __name__ == "__main__":
    main()
