"""
Generation by NGrams starter
"""

from main import GreedyTextGenerator, NGramLanguageModel, TextProcessor

# pylint:disable=too-many-locals, unused-import, unused-variable


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
    encoded_text = text_processor.encode(text)
    if encoded_text is None:
        result = None
    else:
        language_model = NGramLanguageModel(encoded_text, 7)
        if not language_model.build():
            result = None
        else:
            generator = GreedyTextGenerator(language_model, text_processor)
            result = generator.run("Vernon", 51)
            if result is not None:
                print(result)
    assert result


if __name__ == "__main__":
    main()
