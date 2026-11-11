"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from lab_3_generate_by_ngrams.main import (
    BeamSearchTextGenerator,
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

    # if language_model.build():
    #     print(f"N-gram frequencies: {language_model._n_gram_frequencies}")

    greedy_generator = GreedyTextGenerator(
        language_model=language_model,
        text_processor=processor)

    greedy_generated_text = greedy_generator.run(
        prompt="Vernon",
        seq_len=51)
    print(f"Greedy generated text: {greedy_generated_text}")

    beam_generator = BeamSearchTextGenerator(
        language_model=language_model,
        text_processor=processor,
        beam_width=3)

    beam_generated_text = beam_generator.run(
        prompt="Vernon",
        seq_len=56)
    print(f"Beam generated text: {beam_generated_text}")

if __name__ == "__main__":
    main()
