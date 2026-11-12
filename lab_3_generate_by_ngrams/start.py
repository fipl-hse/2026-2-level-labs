"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable


from lab_3_generate_by_ngrams.main import (
    TextProcessor,
    NGramLanguageModel,
    GreedyTextGenerator,
    BeamSearchTextGenerator
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
    encoded_text = processor.encode(text)
    if encoded_text is not None:
        processor.decode(encoded_text)
    result = None
    if encoded_text:
        model_n7 = NGramLanguageModel(encoded_text, 7)
        model_n7.build()
        greedy_generator = GreedyTextGenerator(model_n7, processor)
        greedy_result = greedy_generator.run('Vernon', 51)
        print(f"Greedy N=7: {greedy_result}")
        beam_generator = BeamSearchTextGenerator(model_n7, processor, beam_width=3)
        result = beam_generator.run('Vernon', 56)
        print(f"Beam Search N=7 (beam=3): {result}")
    assert result


if __name__ == "__main__":
    main()
