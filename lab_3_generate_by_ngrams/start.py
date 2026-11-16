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

    print('Mark 4 task')

    text_processor = TextProcessor('_')
    encoded_text = text_processor.encode(text)
    if encoded_text is None:
        return

    decoded_text = text_processor.decode(encoded_text)
    if decoded_text is None:
        return

    print(
        f'Encoded text:\n{encoded_text[-100:]}\n\n'
        f'Decoded text:\n{decoded_text[-100:]}'
    )

    print('\nNGram LM check task')

    model = NGramLanguageModel(encoded_text, 7)
    print('Model built:', model.build())

    print('\nMark 6 task')

    greedy_generator = GreedyTextGenerator(model, text_processor)
    generated_text = greedy_generator.run('Vernon', 51)
    print('Generated text:')
    print(generated_text)

    print('\nMark 8 task')
    generator = BeamSearchTextGenerator(
        language_model=model,
        text_processor=text_processor,
        beam_width=3,
    )
    generated = generator.run('Vernon', 56)
    print('Generated text:')
    print(generated)

    print('\nMark 10 task 1')
    reader = NGramLanguageModelReader(
        "./lab_3_generate_by_ngrams/assets/en_own.json", '_'
    )
    models = []
    for ngram_size in (2, 3, 4):
        loaded_model = reader.load(ngram_size)
        if loaded_model is not None:
            models.append(loaded_model)

    backoff_generator = BackOffGenerator(
        tuple(models),
        reader.get_text_processor(),
    )
    backoff_generated = backoff_generator.run('Vernon', 100)
    print(backoff_generated)

    print('\nMark 10 task 2')
    prompt = 'Harry looked at'

    word_processor = WordProcessor('<eos>')
    encoded_text_2 = word_processor.encode(text)
    if encoded_text_2 is None:
        return

    word_models = {}
    for ngram_size in (2, 3, 4):
        word_model = NGramLanguageModel(encoded_text_2, ngram_size)
        word_model.build()
        word_models[ngram_size] = word_model

    print(
        '\nGreedy algorithm continue:\n'
        f'{GreedyTextGenerator(word_models[4], word_processor).run(prompt, 12)}'
    )

    beam_continue = BeamSearchTextGenerator(
        language_model=word_models[4],
        text_processor=word_processor,
        beam_width=3,
    )
    print(f'\nBeam Search algorithm continue:\n{beam_continue.run(prompt, 12)}')

    backoff_continue = BackOffGenerator(
        tuple(word_models.values()),
        word_processor,
    )
    print(f'\nBackOff algorithm continue:\n{backoff_continue.run(prompt, 12)}')

    print(
        '\nComparison to greedy generated text at the level of letters:\n'
        f'{greedy_generator.run(prompt, 60)}'
    )

    result = backoff_generated
    assert result

    processor = TextProcessor("_")

    encoded_text = processor.encode(text)
    assert encoded_text, "Text can not be encoded"
    print("Закодированный текст: ", encoded_text[:101])

    decoded_text =  processor.decode(encoded_text)
    assert decoded_text, "Text can not be decoded"
    print("Раскодированный текст: ", decoded_text[:101])

    n_gram_lang_model = NGramLanguageModel(encoded_text, 7)
    n_gram_freq = n_gram_lang_model.build()
    print("Построенная модель: ", n_gram_lang_model.build())
    assert n_gram_freq, "Model can not be build"

    greedy_text_generator = GreedyTextGenerator(n_gram_lang_model, processor)
    result_greedy_generator = greedy_text_generator.run("Vernon", 51)
    assert result_greedy_generator, "Impossible to generate text"
    print("Результат GreedyGenerator: ", result_greedy_generator)

    beam_search_generator = BeamSearchTextGenerator(n_gram_lang_model, processor, 7)
    result_beam_generator = beam_search_generator.run("Vernon", 56)
    assert result_beam_generator, "Impossible to generate text"
    print("Результат BeamSearchGenerator: ", result_beam_generator)

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
    print("Результат BackOffGenerator: ", result_backoff_generator)

    word_processor = WordProcessor("<eos>")
    encoded_words = word_processor.encode(text)

    word_models = []
    for n_gram_size in (2, 3, 4):
        word_model = NGramLanguageModel(encoded_words, n_gram_size)
        assert word_model.build() is not None, "Model can not be build"
        print(
            f"Построенная по словам модель({n_gram_size}): ",
            word_model.build(),
        )
        word_models.append(word_model)

    prompt = "Harry looked at"

    greedy_text_generator_word = GreedyTextGenerator(word_models[-1], word_processor)
    result_greedy_generator_word = greedy_text_generator_word.run(prompt, 12)
    print("Результат GreedyGenerator (слова): ", result_greedy_generator_word)

    beam_search_generator_words = BeamSearchTextGenerator(
        word_models[-1], word_processor, 3
    )
    result_beam_generator_words = beam_search_generator_words.run(prompt, 12)
    print("Результат BeamSearchGenerator (слова): ", result_beam_generator_words)

    back_off_generator_words = BackOffGenerator(tuple(word_models), word_processor)
    result_backoff_generator_words = back_off_generator_words.run(prompt, 12)
    print("Результат BackOffGenerator (слова): ", result_backoff_generator_words)

    result_greedy_letters = greedy_text_generator.run(prompt, 60)
    print("Результат GreedyGenerator (буквы): ", result_greedy_letters)

if __name__ == "__main__":

    main()
