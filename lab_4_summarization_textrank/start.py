"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code
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
    with open(
        "lab_4_summarization_textrank/assets/article_701.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()
    with open(
        "lab_4_summarization_textrank/assets/stop_words.txt", "r", encoding="utf-8"
    ) as text_file:
        stop_words = tuple(text_file.read().split("\n"))

    punctuation = ('.', ',', '!', '?')
    sentence_preprocessor = SentencePreprocessor(stop_words, punctuation)
    preprocessed_sentences = sentence_preprocessor.get_sentences(text)
    assert preprocessed_sentences, 'Preprocession failed'
    print('Preprocessed sentences:', preprocessed_sentences)

    sentence_encoder = SentenceEncoder()
    sentence_encoder.encode_sentences(preprocessed_sentences)

    graph = TextGraph()
    graph.build(preprocessed_sentences)

    summarizer = NaiveSummarizer(graph)
    result = summarizer.summarize(5)
    print(result)

    assert result


if __name__ == "__main__":
    main()
