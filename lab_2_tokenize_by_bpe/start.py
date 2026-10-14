"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    decode,
    get_vocabulary,
    prepare_word,
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

    word_frequencies = collect_frequencies(text, None, "</s>")
    assert word_frequencies, "Translation not working"

    trained_tokenizator = train(word_frequencies, 100)
    assert trained_tokenizator

    vocabulary = get_vocabulary(trained_tokenizator, "<unk>")

    secret_text = [int(el) for el in secret_text.split()]
    decoded_text = decode(secret_text, vocabulary, "</s>")

    print(decoded_text)
    return None


if __name__ == "__main__":
    main()
