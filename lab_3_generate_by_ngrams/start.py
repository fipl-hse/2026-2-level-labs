"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from main import GreedyTextGenerator, NGramLanguageModel, TextProcessor


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

    processor = TextProcessor("_")

    encoded_text = processor.encode(text)

    result = processor.decode(encoded_text)

    n_gramm = NGramLanguageModel(encoded_text, 7)
    mle = n_gramm.build()

    textgenerator = GreedyTextGenerator(n_gramm, processor)
    generated_text = textgenerator.run('Vernon', 51)

    print(generated_text)

    assert result


if __name__ == "__main__":
    main()
