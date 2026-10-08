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

    freq_dict = collect_frequencies(text, None, "</s>")
    print(f"Demonstration of frequency dictionary: {freq_dict}")

    trains = train(freq_dict, 100)
    print(f"Demonstration of trained tokenizer: {trains}")

    vocabulary = get_vocabulary(trains, "<unk>")
    print(f"Vocabulary size: {len(vocabulary)}")

    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_5.txt", "r", encoding="utf-8") as secret_file:
        secret_content = secret_file.read()

    encoded_numbers = [int(x) for x in secret_content.split()]

    decoded_text = decode(encoded_numbers, vocabulary, "</s>")
    print(f"Decoded secret: {decoded_text}")
    assert decoded_text, "Translation not working"


if __name__ == "__main__":
    main()
