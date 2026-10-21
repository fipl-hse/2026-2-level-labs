"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from main import (
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
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8") as text_file:
        secret_text = text_file.read()

    freqs = collect_frequencies(text, None, "</s>")
    assert freqs is not None
    tokenizer = train(freqs, 100)
    assert tokenizer is not None
    vocabulary = get_vocabulary(tokenizer, "<unk>")
    assert vocabulary is not None
    secret_text = [int(el) for el in secret_text.split()]
    result = decode(secret_text, vocabulary, "</s>")
    assert result, "Translation not working"
    print(result)


if __name__ == "__main__":
    main()