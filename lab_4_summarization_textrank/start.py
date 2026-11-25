"""
TextRank summarizer starter
"""

# pylint:disable=unused-variable, unused-import, duplicate-code
from lab_4_summarization_textrank.main import (
    NaiveSummarizer,
    SentenceEncoder,
    SentencePreprocessor,
    TextGraph,
    TextRankSummarizer,
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
    preprocessor = SentencePreprocessor(stop_words, [".", "!", "?"])
    result = preprocessor.get_sentences(text)

    encoder = SentenceEncoder()
    encoder.encode_sentences(result)
    for index, sentence in enumerate(result, 1):
        print(f"""{index}. Sentence: {sentence.get_text()}
            \nEncoded sentence: {sentence.get_encoded()}""")

    graph = TextGraph()
    graph.build(result)

    summuriser_naive = NaiveSummarizer(graph)
    summuriser_text_rank= TextRankSummarizer(graph)
    summuriser_text_rank.train()

    for idx, algorythm in enumerate((summuriser_naive, summuriser_text_rank), 1):
        print (f"{idx}. Summary: {algorythm.summarize(5)}")
    assert result


if __name__ == "__main__":
    main()
