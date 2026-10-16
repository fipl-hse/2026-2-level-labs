"""
BPE Tokenizer starter
"""

from lab_2_tokenize_by_bpe.main import (
    calculate_bleu,
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
    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as text_file:
        ru_text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/ru_encoded.txt", "r", encoding="utf-8") as text_file:
        encoding_ref = [int(i) for i in text_file.read().split()]
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = [int(x) for x in text_file.read().split()]
    with open(
        "lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt",
        "r",
        encoding="utf-8") as text_file:
        secret_text = [int(x) for x in text_file.read().split()]

    freq_by_words = collect_frequencies(text, None, "</s>")
    tokenized_words = train(freq_by_words, 100)
    if tokenized_words is None:
        return None
    ru_vocab = get_vocabulary(tokenized_words, "<unk>")
    if ru_vocab is None:
        return None
    decoded_secret = decode(secret_text, ru_vocab, "</s>")
    print(decoded_secret)

    print()

    translation_vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    ru_encoded = encode(
        ru_text,
        translation_vocab,
        start_of_word_token="\u2581",
        end_of_word_token=None,
        unknown_token="<unk>"
    )
    if ru_encoded is None:
        return None
    print(all(ru_encoded[i] == encoding_ref[i] for i in range(20)))

    decoded_predictions = decode(
        translation_encoded_raw,
        translation_vocab,
        None
    )

    if decoded_predictions is None:
        return None
    decoded_predictions = decoded_predictions.replace("\u2581", " ")

    result = calculate_bleu(
        decoded_predictions,
        text_reference_translation,
    )
    print(decoded_predictions)
    print(result)

    assert result, "Translation not working"
    return None


if __name__ == "__main__":
    main()
