"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import(
    collect_frequencies,
    decode,
    get_vocabulary,
    train,
)


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_3.txt", "r", encoding="utf-8") as text_file:
        secret3 = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read()

    result = collect_frequencies(text, None, "</s>")

    assert result, "Frequency dictionary is None"
    # print(result)

    bpe_train = train(result, 100)

    assert bpe_train, "Train is None"
    # print(bpe_train)

    vocabulary = get_vocabulary(bpe_train,'<unk>')
    assert vocabulary, "Voc is None"

    secret3 = [int(number) for number in secret3.split()]
    secret = decode(secret3, vocabulary, '</s>')
    assert decode, "Decode is None"
    print(secret)


if __name__ == "__main__":
    main()
