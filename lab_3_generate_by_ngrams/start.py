"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable

from lab_3_generate_by_ngrams.main import (
    BeamSearchTextGenerator,
    GreedyTextGenerator,
    TextProcessor,
    NGramLanguageModel
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
    result = processor.decode(encoded)
    print("Greedy Text Generator")
    n_gram_size = int(input("Введите размер н-граммы: "))
    model = NGramLanguageModel(encoded, n_gram_size)
    build_result = model.build()
    frequencies = model._n_gram_frequencies
    for i, (n_gram, prob) in enumerate(frequencies.items()):
        if i >= 10:
            break
        print(f"  {n_gram}: {prob}")
    #n_gram_size = model.get_n_gram_size()
    #print(n_gram_size)

    generator = GreedyTextGenerator(model, processor)
    prompt = input("Введите промпт для генерации текста: ")
    seq_len =  int(input("Введите количество токенов для генерации: "))
    generated = generator.run(prompt, seq_len)
    print(f"Generated: {generated}")

    print("Beam Search Text Generator")
    n_gram_size2 = int(input("Введите размер н-граммы: "))
    beamgenerator = BeamSearchTextGenerator(model, processor, n_gram_size2)
    prompt2 =  input("Введите промпт для генерации текста: ")
    seq_len2 =  int(input("Введите количество токенов для генерации: "))
    generated2 = beamgenerator.run(prompt2, seq_len2)
    print(f"Generated: {generated2}")

    assert result



if __name__ == "__main__":
    main()
