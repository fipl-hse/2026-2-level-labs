"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable

import json

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
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()

    processor = TextProcessor('_')
    encoded_text = processor.encode(text[:100])
    print(encoded_text)

    if encoded_text is not None:
        decoded_text = processor.decode(encoded_text)
        print(decoded_text)

        result = decoded_text
    else:
        result = None


    encoded_for_model = processor.encode(text)

    if encoded_for_model is not None:
        model = NGramLanguageModel(encoded_for_model, 3)
        is_built = model.build()

        print("Модель:", is_built)
        print("Частотный словарь n-грамм:")
        frequencies = getattr(model, '_n_gram_frequencies', None)
        print(frequencies)

    if encoded_for_model is not None:
        model_7 = NGramLanguageModel(encoded_for_model, 7)
        model_7.build()
        greedy_generator = GreedyTextGenerator(model_7, processor)
        generated_text = greedy_generator.run('Vernon', 51)
        print('Result:')
        print(generated_text)

    if encoded_for_model is not None:
        model_beam = NGramLanguageModel(encoded_for_model, 7)
        model_beam.build()
        beam_generator = BeamSearchTextGenerator(model_beam, processor, beam_width=3)
        beam_result = beam_generator.run('Vernon', 56)
        print('Result of Beam Search:')
        print(beam_result)
        result = beam_result

    assert result



if __name__ == "__main__":
    main()
