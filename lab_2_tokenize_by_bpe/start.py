"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

from main import collect_frequencies, decode, get_vocabulary, train


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
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8") as text_file:
        secret_text = [int(x) for x in text_file.read().split()]

    result = None

    freq_dict = collect_frequencies(text, None, "</s>")
    print(f"Demonstration of frequency dictionary: {freq_dict}")

    result = train(freq_dict, 100)
    print(f"Demonstration of trained tokenizer: {result}")

    ru_vocab = get_vocabulary(result, "<unk>")
    if ru_vocab is None:
        return None
    decoding_result = decode(secret_text, ru_vocab, "</s>" )
    print(f"Demonstration of the decoding algorithm: {decoding_result}")

    assert result, "Translation not working"


if __name__ == "__main__":
    main()
