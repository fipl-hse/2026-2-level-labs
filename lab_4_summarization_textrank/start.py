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

    stop_words = ('в', 'на', 'и')
    punctuation = ('.', ',', '!', '?')
    sentence_preprocessor = SentencePreprocessor(stop_words, punctuation)
    preprocessed_sentences = sentence_preprocessor.get_sentences(text)
    assert preprocessed_sentences, 'Preprocession failed'
    print('Preprocessed sentences:', preprocessed_sentences)

    sentence_encoder = SentenceEncoder()
    encoded_sentences = sentence_encoder.encode_sentences(preprocessed_sentences)
    assert encoded_sentences, 'Encoding failed'
    print('Encoded sentences:', encoded_sentences)

    # assert result
    # it's for me not to forget assert result


if __name__ == "__main__":
    main()
