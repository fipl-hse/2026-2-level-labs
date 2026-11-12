"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from lab_3_generate_by_ngrams.main import (
    BeamSearchTextGenerator,
    GreedyTextGenerator,
    NGramLanguageModel,
    TextProcessor,
    NGramLanguageModelReader,
    BackOffGenerator
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
    result_greedy_generator = greedy_text_generator.run("Vernon", 51)
    assert result_greedy_generator, "Impossible to generate text"
    print(result_greedy_generator)

    beam_search_generator = BeamSearchTextGenerator(n_gram_lang_model, processor, 7)
    result_beam_generator = beam_search_generator.run("Vernon", 56)
    assert result_beam_generator, "Impossible to generate text"
    print(result_beam_generator)

    reader = NGramLanguageModelReader("./lab_3_generate_by_ngrams/assets/en_own.json", "_")
    language_models = []

    for n_gram_size in (2, 3, 4):
        model = reader.load(n_gram_size)
        if model is not None:
            language_models.append(model)

    language_models = tuple(language_models)

    back_off_generator = BackOffGenerator(language_models, reader.get_text_processor())
    result_backoff_generator = back_off_generator.run("Vernon", 100)
    assert result_backoff_generator, "Text can not be generated"
    print(result_backoff_generator)

if __name__ == "__main__":

    main()
