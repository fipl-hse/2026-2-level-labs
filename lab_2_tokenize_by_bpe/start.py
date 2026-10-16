"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable


from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    decode,
    encode,
    get_vocabulary,
    load_vocabulary,
    train,
)


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as text_file:
        russian_text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/ru_encoded.txt", "r", encoding="utf-8") as text_file:
        russian_encoded_reference = text_file.read()


    freq_dict = collect_frequencies(text, None, '</s>')
    trained_freq = train(freq_dict, 100)

    if trained_freq is None:
        return

    vocabulary = get_vocabulary(trained_freq, '<unk>')
    encoded = [int(token_id) for token_id in translation_encoded_raw.replace(',', ' ').split()]
    result = decode(encoded, vocabulary, '</s>')
    print(result)

    assert result, "Translation not working"

    load_vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    rus_encoded = encode(russian_text, load_vocab, '\u2581', None, '<unk>')

    print(f'First 20 tokens: {rus_encoded}')
    print(f'Reference first 20 tokens: {russian_encoded_reference}')

if __name__ == "__main__":
    main()
