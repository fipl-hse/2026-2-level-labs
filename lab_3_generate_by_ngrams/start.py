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
    processor = TextProcessor("_")
    encoded_text = processor.encode(text)
    decoded_text = processor.decode(encoded_text)
    print(decoded_text)
    language_model = NGramLanguageModel(encoded_text, 7)
    language_model.build()
    greedy_generator = GreedyTextGenerator(language_model, processor)
    result = greedy_generator.run("Vernon", 51)
    assert result
    print(result)


if __name__ == "__main__":
    main()
