"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from lab_3_generate_by_ngrams.main import GreedyTextGenerator, NGramLanguageModel, TextProcessor


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()

    processor = TextProcessor("_")

    encoded_text = processor.encode(text)
    assert encoded_text, "Text can not be encoded"
    print(encoded_text[:101])

    decoded_text =  processor.decode(encoded_text)
    assert decoded_text, "Text can not be decoded"
    print(decoded_text[:101])

    n_gram_lang_model = NGramLanguageModel(encoded_text, 7)
    n_gram_freq = n_gram_lang_model.build()
    print(n_gram_freq)

    greedy_text_generator = GreedyTextGenerator(n_gram_lang_model, processor)
    result = greedy_text_generator.run("Vernon", 51)
    assert result, "Impossible to generate text"
    print(result)

if __name__ == "__main__":
    main()
