"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from main import collect_frequencies, get_vocabulary, decode


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
    freqs = collect_frequencies(secret_1, None, "</s>")
    vocab = get_vocabulary(freqs, "<unk>")
    text = decode(secret_1, vocab, "</s>")
    result = None
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
