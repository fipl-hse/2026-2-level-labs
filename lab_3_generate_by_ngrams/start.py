"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from lab_3_generate_by_ngrams.main import (
    BackOffGenerator,
    BeamSearchTextGenerator,
    GreedyTextGenerator,
    NGramLanguageModel,
    NGramLanguageModelReader,
    TextProcessor,
    WordProcessor,
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
    print("Encoded text: ", encoded_text[:101])

    decoded_text =  processor.decode(encoded_text)
    assert decoded_text, "Text can not be decoded"
    print("Decoded text: ", decoded_text[:101])

    n_gram_lang_model = NGramLanguageModel(encoded_text, 7)
    n_gram_freq = n_gram_lang_model.build()
    print("Builded model: ", n_gram_lang_model.build())
    assert n_gram_freq, "Model can not be build"

    greedy_text_generator = GreedyTextGenerator(n_gram_lang_model, processor)
    result_greedy_generator = greedy_text_generator.run("Vernon", 51)
    assert result_greedy_generator, "Impossible to generate text"
    print("Result of GreedyGenerator: ", result_greedy_generator)

    beam_search_generator = BeamSearchTextGenerator(n_gram_lang_model, processor, 7)
    result_beam_generator = beam_search_generator.run("Vernon", 56)
    assert result_beam_generator, "Impossible to generate text"
    print("Result of BeamSearchGenerator: ", result_beam_generator)

    reader = NGramLanguageModelReader("./lab_3_generate_by_ngrams/assets/en_own.json", "_")
    language_models_lst = []

    for n_gram_size in (2, 3, 4):
        model = reader.load(n_gram_size)
        if model is not None:
            language_models_lst.append(model)

    language_models = tuple(language_models_lst)

    back_off_generator = BackOffGenerator(language_models, reader.get_text_processor())
    result_backoff_generator = back_off_generator.run("Vernon", 100)
    assert result_backoff_generator, "Text can not be generated"
    print("Result BackOffGenerator: ", result_backoff_generator)
    print("Statistics: ", back_off_generator.freq_of_size_model)

    word_processor = WordProcessor("<eos>")
    encoded_words = word_processor.encode(text)

    word_models = []
    for n_gram_size in (2, 3, 4, 5, 6):
        word_model = NGramLanguageModel(encoded_words, n_gram_size)
        assert word_model.build() is not None, "Model can not be build"
        print(
            f"Model, builded by words ({n_gram_size}): ",
            word_model.build(),
        )
        word_models.append(word_model)

    prompt = "Harry looked"

    greedy_text_generator_word = GreedyTextGenerator(word_models[-1], word_processor)
    result_greedy_generator_word = greedy_text_generator_word.run(prompt, 12)
    print("Result GreedyGenerator by words: ", result_greedy_generator_word)

    beam_search_generator_words = BeamSearchTextGenerator(
        word_models[-1], word_processor, 3
    )
    result_beam_generator_words = beam_search_generator_words.run(prompt, 12)
    print("Result BeamSearchGenerator by words: ", result_beam_generator_words)

    back_off_generator_words = BackOffGenerator(tuple(word_models), word_processor)
    result_backoff_generator_words = back_off_generator_words.run(prompt, 12)
    print("Result BackOffGenerator by words: ", result_backoff_generator_words)

    result_greedy_letters = greedy_text_generator.run(prompt, 60)
    print("Result GreedyGenerator by letters: ", result_greedy_letters)

if __name__ == "__main__":

    main()
