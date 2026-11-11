"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from main import (
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
    # result = None
    # assert result

    text_processor = TextProcessor("_")

    encoded_corpus = text_processor.encode(text)
    # print("Encoded text(the first 50 numbers):")
    # print(encoded_corpus[:50])
    # assert encoded_corpus, "encoded text is None"

    # decoded_corpus = text_processor.decode(encoded_corpus)
    # print("Decoded text (the first 200 chars):")
    # print(decoded_corpus[:200])
    # assert decoded_corpus, "decoded text is None"

    #mark6
    language_model = NGramLanguageModel(encoded_corpus, 7)

    build_model = language_model.build()
    assert build_model, "failed to build the language model"

    generator = GreedyTextGenerator(language_model, text_processor)
    result = generator.run("Vernon", 51)
    print(result)

    #mark8
    beam_search_generator = BeamSearchTextGenerator(language_model, text_processor, 7)
    result_beam = beam_search_generator.run("Vernon", 56)
    #assert result_beam, "Impossible to generate text"
    print(result_beam)


if __name__ == "__main__":
    main()
