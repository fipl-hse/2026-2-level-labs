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

    text_processor = TextProcessor("_")
    encoded_corpus = text_processor.encode(text)
    assert encoded_corpus is not None, "The text could not be encoded"

    decoded_text = text_processor.decode(encoded_corpus)
    assert decoded_text is not None, "The text could not be decoded"

    language_model = NGramLanguageModel(encoded_corpus, 7)
    assert language_model.build() is True, "The language model could not be built"

    greedy_generator = GreedyTextGenerator(language_model, text_processor)
    greedy_text = greedy_generator.run("Vernon", 51)
    assert greedy_text is not None, " The Greedy generation is failed"

    beam_generator = BeamSearchTextGenerator(language_model, text_processor, 3)
    beam_text = beam_generator.run("Vernon", 56)
    assert beam_text is not None, "The Beam Search Generation is failed"

    result = beam_text
    assert result

if __name__ == "__main__":
    main()
