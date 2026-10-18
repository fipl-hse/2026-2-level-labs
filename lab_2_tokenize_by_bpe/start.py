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
        secret_1 = text_file.read()
    freqs = collect_frequencies(text, None, "</s>")
    freqs = train(freqs, 1000)          # подставь нужное число merge'ей
    vocab = get_vocabulary(freqs, "<unk>")
    encoded_secret = [int(token) for token in secret_1.split()]
    result = decode(encoded_secret, vocab, "</s>")
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
