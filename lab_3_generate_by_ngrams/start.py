"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable


from main import TextProcessor, NGramLanguageModel, GreedyTextGenerator


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()
    # result = None
    # assert result

    # Mark 4

    processing_text = TextProcessor(end_of_word_token = "_")
    encoded_text = processing_text.encode(text)
    print(encoded_text)
    decoded_text = processing_text.decode(encoded_text)
    print(decoded_text)

    # N-grams frequencies dictionary

    building_freq_dict = NGramLanguageModel(encoded_text, n_gram_size = 7)
    frequency_dictionary = building_freq_dict.build()
    print(frequency_dictionary)
    print(building_freq_dict._n_gram_frequencies)

    # Mark 6

    greedy_text_generator = GreedyTextGenerator(building_freq_dict, processing_text)
    prompt = "Vernon"
    seq_len = 51
    result = greedy_text_generator.run(prompt, seq_len)
    print(f"Затравка: '{prompt}'")
    print(f"Результат генерации (длина {seq_len}):")
    print(result)

if __name__ == "__main__":
    main()
