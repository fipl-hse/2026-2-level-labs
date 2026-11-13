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
    result = None

    processor = TextProcessor("_")

    encoded_text = processor.encode(text)
    if not isinstance(encoded_text, tuple):
        return None

    result = processor.decode(encoded_text)

    n_gramm = NGramLanguageModel(encoded_text, 7)
    mle = n_gramm.build()

    textgenerator = GreedyTextGenerator(n_gramm, processor)
    generated_text = textgenerator.run('Vernon', 51)

    print(generated_text)

    beam_search_generator = BeamSearchTextGenerator(n_gramm, processor, 3)

    generated_text_beam_search = beam_search_generator.run('Vernon', 56)
    print(generated_text_beam_search)

    assert result
    return None


if __name__ == "__main__":
    main()
