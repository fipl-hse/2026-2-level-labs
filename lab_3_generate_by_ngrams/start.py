"""
Generation by NGrams starter
"""

from lab_3_generate_by_ngrams.main import (
    TextProcessor,
    NGramLanguageModel,
    GreedyTextGenerator,
)


def main() -> None:
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt",
        "r",
        encoding="utf-8"
    ) as text_file:
        text = text_file.read()

    text_processor = TextProcessor('<eow>')


    encoded = tuple(text_processor.encode(text))

    print(f'Encoded corpus size: {len(encoded)}')

    language_model = NGramLanguageModel(encoded, 2)
    is_built = language_model.build()
    print(f'Is built: {is_built}')

    if is_built:
        print(list(language_model._n_gram_frequencies.items())[:10])
    else:
        print("Ошибка: Модель не построилась. Проверьте метод build() в main.py")
        return


    language_model = NGramLanguageModel(encoded, 7)
    language_model.build()

    generator = GreedyTextGenerator(language_model, text_processor)
    print(generator.run('Vernon', 51))


if __name__ == "__main__":
    main()