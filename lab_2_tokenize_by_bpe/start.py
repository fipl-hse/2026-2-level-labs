"""
BPE Tokenizer starter
"""

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    train,
    get_vocabulary,
    decode,
)


# pylint:disable=too-many-locals, unused-variable


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

    frequencies = collect_frequencies(text, None, "</s>")
    trained = train(frequencies, 100)
    vocabulary = get_vocabulary(trained, "<unk>")

    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8") as f:
        encoded = [int(x) for x in f.read().split()]

    result = decode(encoded, vocabulary, "</s>")
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
