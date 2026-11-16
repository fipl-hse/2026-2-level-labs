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
    "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()

    processor = TextProcessor("_")
    encoded = processor.encode(text)
    if encoded is None:
        return
    result = processor.decode(encoded)
    print("Greedy Text Generator")
    model = NGramLanguageModel(encoded, 7)
    build_result = model.build()

    generator = GreedyTextGenerator(model, processor)
    generated = generator.run('Vernon', 51)
    print(f"Generated: {generated}")
    print("Beam Search Text Generator")
    beamgenerator = BeamSearchTextGenerator(model, processor, 7)
    generated2 = beamgenerator.run('Vernon', 56)
    print(f"Generated: {generated2}")

    assert result

if __name__ == "__main__":
    main()
