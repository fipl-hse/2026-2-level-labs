"""
Generation by NGrams starter
"""

from main import NGramLanguageModel, TextProcessor


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()
    result = None
    text_processor = TextProcessor('_')
    encoded_corpus = text_processor.encode(text)
    n_gram_language_model = NGramLanguageModel(encoded_corpus, n_gram_size=3)
    result = n_gram_language_model.build()
    print(result)
    assert result


if __name__ == "__main__":
    main()