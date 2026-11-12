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

    text_processor = TextProcessor("_")
    encoded_text = text_processor.encode(text)
    decoded_text = text_processor.decode(encoded_text)

    model = NGramLanguageModel(encoded_text, 7)
    build_example =model.build()
    print(f"build example : {build_example}")
    freq_example = model._n_gram_frequencies
    print(f"frequencies example: {freq_example}")

    generator = GreedyTextGenerator(model, text_processor)
    generated = generator.run("Vernon", 51)
    print(f"greedy generated: {generated}")
    result = generated
    assert result



if __name__ == "__main__":
    main()
