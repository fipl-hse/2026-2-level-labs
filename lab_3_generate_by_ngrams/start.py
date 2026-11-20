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

    tp = TextProcessor('_')
    encoded_text = tp.encode(text)
    assert encoded_text is not None

    model = NGramLanguageModel(encoded_text, 7)
    assert model.build() is True

    generator = GreedyTextGenerator(model, tp)

    generated_text = generator.run("Vernon", 51)
    assert generated_text is not None

    decoded_text = tp.decode(encoded_text)
    assert decoded_text is not None

    print("Original text (first 100 chars):", text[:100])
    print("Encoded text (first 50 ids):", encoded_text[:50])
    print("Decoded text (first 100 chars):", decoded_text[:100])

    print(generated_text)

    result = generated_text
    assert result


if __name__ == "__main__":
    main()
