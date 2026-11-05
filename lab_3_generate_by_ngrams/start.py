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

    print('Mark 4 task')

    text_processor = TextProcessor('_')
    encoded_text = text_processor.encode(text)
    if encoded_text is None:
        return

    decoded_text = text_processor.decode(encoded_text)
    if decoded_text is None:
        return

    print('Encoded text:')
    print(encoded_text[-100:])
    print('Decoded text:')
    print(decoded_text[-100:])

    result = decoded_text
    assert result

    print('NGram LM check task')

    model = NGramLanguageModel(encoded_text, 7)
    is_freq_dict_built = model.build()

    print('Model built:', is_freq_dict_built)

    print('Mark 6 task')

    greedy_generator = GreedyTextGenerator(model, text_processor)
    generated_text = greedy_generator.run('Vernon', 51)
    print('Generated text:')
    print(generated_text)

if __name__ == "__main__":
    main()
