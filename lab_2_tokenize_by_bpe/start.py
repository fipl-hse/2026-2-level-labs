"""
BPE Tokenizer starter
"""

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    decode,
    encode,
    get_vocabulary,
    load_vocabulary,
    train,
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
    with open(
            "lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt",
            "r",
            encoding="utf-8"
    ) as text_file:
        secret_1_raw = text_file.read()
    result = None


    #mark 4
    result_4 = collect_frequencies(text, start_of_word = None, end_of_word = "</s>")
    assert result_4, "Frequencies not collected"
    print(result_4)
    assert result_4, "Translation not working"

    #mark 6
    machine_train = train(result_4, 100)
    assert machine_train, "Training not working"
    vocabulary = get_vocabulary(machine_train,'<unk>')
    assert vocabulary, "Vocabulary not working"
    secret_1_unpacked =[int(number) for number in secret_1_raw.split()]
    secret_1_encoded = decode(secret_1_unpacked, vocabulary, '</s>')
    assert secret_1_encoded, "Decoding not working"
    print(secret_1_encoded)

    #mark 8
    vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")

    assert vocab, "Vocabulary not loaded"

    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as text_file:
        ru_text = text_file.read()

    encoded_russian = encode(ru_text, vocab, "\u2581", None, "<unk>")
    assert encoded_russian, "Encoding not working"
    result_8 = encoded_russian
    print(result_8)




    assert result_8, "Translation not working"


if __name__ == "__main__":
    main()
