"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable

from lab_3_generate_by_ngrams.main import (
    GreedyTextGenerator,
    NGramLanguageModel,
    TextProcessor,
)


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()

    text_processor = TextProcessor("_")
    encoded_corpus = text_processor.encode(text)
    assert encoded_corpus is not None

    sample_size = 200
    encoded_sample = encoded_corpus[:sample_size]
    decoded_sample = text_processor.decode(encoded_sample)
    print("Encoded sample:", encoded_sample)
    print("Decoded sample:", decoded_sample)

    language_model = NGramLanguageModel(encoded_corpus, 7)
    assert language_model.build() is True

    greedy_generator = GreedyTextGenerator(language_model, text_processor)
    greedy_text = greedy_generator.run("Vernon", 51)
    print("Greedy:", greedy_text)

    result = greedy_text
    assert result


if __name__ == "__main__":
    main()
