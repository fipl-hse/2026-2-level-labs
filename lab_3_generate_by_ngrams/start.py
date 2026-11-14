"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable

from lab_3_generate_by_ngrams.main import (
    BeamSearchTextGenerator,
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
    processor = TextProcessor("_")
    encoded = processor.encode(text)
    if not encoded:
        return
    decoded = processor.decode(encoded)
    print(decoded)

    model = NGramLanguageModel(encoded, n_gram_size=7)
    model.build()

    greedy_generator = GreedyTextGenerator(model, processor)
    result = greedy_generator.run("Vernon", 51)
    print(result)

    assert result


if __name__ == "__main__":
    main()
