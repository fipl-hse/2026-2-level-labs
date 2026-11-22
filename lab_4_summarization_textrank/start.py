"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code

from lab_4_summarization_textrank.main import SentencePreprocessor, SentenceEncoder

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

    sentence_processor = SentencePreprocessor(stop_words, (".", "!", "?"))
    extracted_sentences = sentence_processor.get_sentences(text)

    sentence_encoder = SentenceEncoder()
    result = sentence_encoder.encode_sentences(extracted_sentences)
    for sentence in extracted_sentences:
        print(sentence.get_text())
        print(sentence.get_encoded())

    assert result


if __name__ == "__main__":
    main()
