"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    calculate_bleu,
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
        translation_encoded_raw = [int(i) for i in text_file.read().split()]
    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as text_file:
        ru_text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/ru_encoded.txt", "r", encoding="utf-8") as text_file:
        ru_expected = [int(i) for i in text_file.read().split()]

    freq_dict = collect_frequencies(text, None, "</s>")
    if freq_dict is None:
        return

    trains = train(freq_dict, 100)
    if trains is None:
        return

    vocabulary = get_vocabulary(trains, "<unk>")
    if vocabulary is None:
        return

    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_5.txt", "r",
              encoding="utf-8") as secret_file:
        secret_content = secret_file.read()

    encoded_numbers = [int(x) for x in secret_content.split()]

    decoded_text = decode(encoded_numbers, vocabulary, "</s>")
    print(f"Decoded secret: {decoded_text}")

    translated_vocabulary = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if translated_vocabulary is None:
        return
    encoded_tokens = encode(ru_text, translated_vocabulary, "\u2581", None, "<unk>")
    if encoded_tokens is None:
        return

    print("Comparison:", encoded_tokens[:20] == ru_expected[:20])

    predictions_decoded = decode(translation_encoded_raw, translated_vocabulary, None)
    if predictions_decoded is None:
        return

    predictions_decoded = predictions_decoded.replace("\u2581", " ")

    result = calculate_bleu(predictions_decoded, text_reference_translation)
    print(f"The result of metric bleu: {result}")
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
