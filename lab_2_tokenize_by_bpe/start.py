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
    with (
        open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8")
        as text_file
    ):
        secret_text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as text_file:
        ru_original_text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/ru_encoded.txt", "r", encoding="utf-8") as text_file:
        ru_encoded_text = text_file.read()

    word_frequencies = collect_frequencies(text, None, "</s>")
    assert word_frequencies, "Impossible to collect frequencies of words"

    trained_tokenizator = train(word_frequencies, 100)
    assert trained_tokenizator, "Tokenizator can not be trained"

    vocabulary = get_vocabulary(trained_tokenizator, "<unk>")
    assert vocabulary, "Impossible to git vocabulary"

    secret_text_splited = [int(el) for el in secret_text.split()]
    result = decode(secret_text_splited, vocabulary, "</s>")
    assert result, "Text can not be decoded"
    print(result)

    vocabulary = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    assert vocabulary, "There is no vocabulary"

    encoded_text = encode(ru_original_text, vocabulary, "\u2581", None, "<unk>")
    assert encoded_text, "Impossible to encode text"

    ru_encoded_text_splited = [int(element) for element in ru_encoded_text.split()]
    assert ru_encoded_text, "Impossible to rncode ru text"
    print(encoded_text[:20] == list(ru_encoded_text_splited[:20]))

if __name__ == "__main__":
    main()
