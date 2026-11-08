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

    text_processor = TextProcessor("_")
    encoded_corpus = text_processor.encode(text)
    assert encoded_corpus is not None

    sample_size = 200
    encoded_sample = encoded_corpus[:sample_size]
    decoded_sample = text_processor.decode(encoded_sample)
    print("Encoded sample:", encoded_sample)
    print("Decoded sample:", decoded_sample)

    language_model = NGramLanguageModel(encoded_corpus, 7)
    assert language_model.build() is True

    greedy_generator = GreedyTextGenerator(language_model, text_processor)
    greedy_text = greedy_generator.run("Vernon", 51)
    print("Greedy:", greedy_text)

    beam_generator = BeamSearchTextGenerator(language_model, text_processor, 5)
    beam_text = beam_generator.run("Vernon", 56)
    print("Beam search:", beam_text)

    reader = NGramLanguageModelReader("./lab_3_generate_by_ngrams/assets/en_own.json", "_")
    models = tuple(m for n in (2, 3, 4) if (m := reader.load(n)) is not None)
    backoff_generator = BackOffGenerator(models, reader.get_text_processor())
    backoff_text = backoff_generator.run("Vernon", 100)
    print("BackOff:", backoff_text)

    result = backoff_text
    assert result

    print("\n--- Word Level ---")
    word_processor = WordProcessor("<eos>")
    word_encoded = word_processor.encode(text)
    assert word_encoded is not None

    word_model2 = NGramLanguageModel(word_encoded, 2)
    word_model2.build()
    word_model3 = NGramLanguageModel(word_encoded, 3)
    word_model3.build()
    word_model4 = NGramLanguageModel(word_encoded, 4)
    word_model4.build()

    word_greedy = GreedyTextGenerator(word_model4, word_processor)
    print("Word Greedy:", word_greedy.run("Harry looked at", 12))

    word_beam = BeamSearchTextGenerator(word_model4, word_processor, 3)
    print("Word Beam Search:", word_beam.run("Harry looked at", 12))

    word_backoff = BackOffGenerator((word_model2, word_model3, word_model4), word_processor)
    print("Word BackOff:", word_backoff.run("Harry looked at", 12))

    letter_greedy = GreedyTextGenerator(language_model, text_processor)
    print("Letter Greedy:", letter_greedy.run("Harry looked at", 60))


if __name__ == "__main__":
    main()
