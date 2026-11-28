"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code


import string


from lab_4_summarization_textrank.main import SentenceEncoder, SentencePreprocessor, calculate_similarity

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

    punctuation = tuple(string.punctuation)

    preprocessor = SentencePreprocessor(stop_words, punctuation)
    sentences = preprocessor.get_sentences(text)

    encoder = SentenceEncoder()
    encoder.encode_sentences(sentences)

    result = None
    assert result


if __name__ == "__main__":
    main()
