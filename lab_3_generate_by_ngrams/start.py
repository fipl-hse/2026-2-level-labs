"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from lab_3_generate_by_ngrams.main import (
    BackOffGenerator,
    BeamSearchTextGenerator,
    GreedyTextGenerator,
    NGramLanguageModelReader,
    NGramLanguageModel,
    TextProcessor,
    WordProcessor,
)


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
    "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r",
    encoding="utf-8") as file:
        text = file.read()
    # result = None
    # assert result

    processor = TextProcessor('_')

    encoded_text = processor.encode(text)
    assert encoded_text is not None
    print(f"Encoded text: {encoded_text}")

    decoded_text = processor.decode(encoded_text)
    assert decoded_text is not None
    print(f"Decoded text: {decoded_text}")

    language_model = NGramLanguageModel(
        encoded_corpus=encoded_text,
        n_gram_size=7)

    build_model = language_model.build()
    assert build_model, "The language model hasn't built"

    greedy_generator = GreedyTextGenerator(
        language_model=language_model,
        text_processor=processor)

    greedy_generated_text = greedy_generator.run(
        prompt="Vernon",
        seq_len=51)
    print(f"Greedy generated text: {greedy_generated_text}")

    greedy_generated_text = greedy_generator.run(
        prompt="Harry looked at",
        seq_len=60)
    print(f"Letter-level Greedy generated text: {greedy_generated_text}")

    beam_generator = BeamSearchTextGenerator(
        language_model=language_model,
        text_processor=processor,
        beam_width=7)

    beam_generated_text = beam_generator.run(
        prompt="Vernon",
        seq_len=56)
    print(f"Beam generated text: {beam_generated_text}")

    reader = NGramLanguageModelReader(
    json_path="./lab_3_generate_by_ngrams/assets/en_own.json",
    eow_token="_",)

    model_2 = reader.load(2)
    model_3 = reader.load(3)
    model_4 = reader.load(4)

    assert model_2 is not None
    assert model_3 is not None
    assert model_4 is not None

    back_off_generator = BackOffGenerator(
        language_models=(model_2, model_3, model_4),
        text_processor=reader.get_text_processor())

    back_off_generated_text = back_off_generator.run(
        prompt="Vernon",
        seq_len=100)
    print(f"BackOff generated text: {back_off_generated_text}")
    result = back_off_generated_text
    assert result

    # Word-level generation

    word_processor = WordProcessor("<eos>")
    encoded_words = word_processor.encode(text)
    assert encoded_words is not None

    word_model_2 = NGramLanguageModel(
        encoded_corpus=encoded_words,
        n_gram_size=2)
    word_model_2.build()

    word_model_3 = NGramLanguageModel(
        encoded_corpus=encoded_words,
        n_gram_size=3)
    word_model_3.build()

    word_model_4 = NGramLanguageModel(
        encoded_corpus=encoded_words,
        n_gram_size=4)
    word_model_4.build()

    # Greedy generation
    word_greedy_generator = GreedyTextGenerator(
        language_model=word_model_4,
        text_processor=word_processor)

    word_greedy_text = word_greedy_generator.run(
        prompt="Harry looked at",
        seq_len=12)
    print(f"Word-level Greedy: {word_greedy_text}")

    # Beam Search generation
    word_beam_generator = BeamSearchTextGenerator(
        language_model=word_model_4,
        text_processor=word_processor,
        beam_width=3)

    word_beam_text = word_beam_generator.run(
        prompt="Harry looked at",
        seq_len=12)
    print(f"Word-level Beam Search: {word_beam_text}")

    # BackOff generation
    word_backoff_generator = BackOffGenerator(
        language_models=(word_model_2, word_model_3, word_model_4),
        text_processor=word_processor)

    word_backoff_text = word_backoff_generator.run(
        prompt="Harry looked at",
        seq_len=12)
    print(f"Word-level BackOff: {word_backoff_text}")


if __name__ == "__main__":
    main()
