"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code


from lab_4_summarization_textrank.main import SentencePreprocessor


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
    punctuation = ('.', ',', '!', '?', ';', ':', '-', '—', '"', "'", '(', ')', '\n', '\r')
    preprocessor = SentencePreprocessor(stop_words, punctuation)
    sentences = preprocessor.get_sentences(text)
    result_parts = []
    for sentence in sentences[:3]:
        result_parts.append(f"Оригинал: {sentence.get_text()}")
        result_parts.append(f"Токены:  {sentence.get_preprocessed()}\n")
    result = "\n".join(result_parts)
    print(result)
    assert result


if __name__ == "__main__":
    main()
