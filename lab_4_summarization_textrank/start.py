"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code

from pathlib import Path

from lab_4_summarization_textrank.main import (
    NaiveSummarizer,
    SentenceEncoder,
    SentencePreprocessor,
    TextGraph,
)


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    package_dir = Path(__file__).resolve().parent

    with open(
        package_dir / "assets" / "article_701.txt",
        "r",
        encoding="utf-8",
    ) as text_file:
        text = text_file.read()

    with open(
        package_dir / "assets" / "stop_words.txt",
        "r",
        encoding="utf-8",
    ) as text_file:
        stop_words = tuple(text_file.read().split("\n"))

    punctuation = (".", ",", "!", "?", ":", ";")
    sentence_preprocessor = SentencePreprocessor(stop_words, punctuation)
    sentences = sentence_preprocessor.get_sentences(text)

    sentence_encoder = SentenceEncoder()
    sentence_encoder.encode_sentences(sentences)

    graph = TextGraph()
    graph.build(sentences)

    summarizer = NaiveSummarizer(graph)
    result = summarizer.summarize(5)

    print(result)
    assert result


if __name__ == "__main__":
    main()
