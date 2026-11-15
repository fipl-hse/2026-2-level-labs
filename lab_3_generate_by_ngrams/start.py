"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable

from lab_3_generate_by_ngrams.main import (
    BeamSearcher,
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

    processor = TextProcessor('_')

    encoded_text = processor.encode(text)
    assert encoded_text is not None
    print(f"Encoded text: {encoded_text[:30]}")

    decoded_text = processor.decode(encoded_text)
    assert decoded_text is not None
    print(f"Decoded text: {decoded_text[:30]}")

    language_model = NGramLanguageModel(
    encoded_corpus=encoded_text,
    n_gram_size=7)

    print(f"Build algorythm: {language_model.build()}")

    textgenerator = GreedyTextGenerator(language_model, processor)
    generated_text = textgenerator.run('Vernon', 51)

    print(f"Greedy generated text: {generated_text}")

    beam_generator =BeamSearchTextGenerator(language_model, processor, 3)

    result = beam_generator.run("Vernon", 56)
    print(f"Beam generated text: {result}")

    assert result


if __name__ == "__main__":
    main()
