"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable

from lab_3_generate_by_ngrams.main import (
    TextProcessor,
    NGramLanguageModel,
    GreedyTextGenerator,
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


    text_processor = TextProcessor('<eow>')
    encoded = text_processor.encode(text)

    print(f'Encoded corpus size: {len(encoded)}')

    language_model = NGramLanguageModel(encoded, 2)
    print(f'Is built: {language_model.build()}')


    print(list(language_model._n_gram_frequencies.items())[:10])

    language_model_7 = NGramLanguageModel(encoded, 7)
    language_model_7.build()

    generator = GreedyTextGenerator(language_model_7, text_processor)

    result = generator.run('Vernon', 51)
    print(result)

    assert result


if __name__ == "__main__":
    main()