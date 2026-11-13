"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable


from main import (
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
        "./assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()

    text_processor = TextProcessor("_")
    encoded_text = text_processor.encode(text)
    assert encoded_text is not None

    print("Кодирование:")
    print(encoded_text)

    print("\nДекодирование")
    print(text_processor.decode(encoded_text))

    sample_text = (1, 2, 3, 0, 4, 1, 0, 2, 5, 6, 6, 7, 0, 2, 3, 0, 4, 1, 0, 2, 5, 6, 6, 7, 0)

    sample_model = NGramLanguageModel(sample_text, 3)
    assert sample_model.build()

    print("\nРезультат работы модели:")
    print(sample_model._n_gram_frequencies)

    language_model = NGramLanguageModel(encoded_text, 7)
    assert language_model.build()

    generator = GreedyTextGenerator(language_model, text_processor)
    result = generator.run(prompt="Vernon", seq_len=51)
    assert result

    print("\nРезультат генерации:")
    print(result)


if __name__ == "__main__":
    main()
