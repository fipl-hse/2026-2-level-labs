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

    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as text_file:
        text_to_translate = text_file.read()

    with open("lab_2_tokenize_by_bpe/assets/ru_encoded.txt", "r", encoding="utf-8") as text_file:
        reference = [int(value) for value in text_file.read().split()]

    secret_path = "lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt"
    with open(secret_path, "r", encoding="utf-8") as secret_file:
        raw_content = secret_file.read()

    encoded_secret = []
    for value in raw_content.split():
        if value.lstrip("-").isdigit():
            encoded_secret.append(int(value))

    word_frequencies = collect_frequencies(text, None, "</s>")

    trained_frequencies = train(word_frequencies, 100)

    vocabulary = get_vocabulary(trained_frequencies, "<unk>") if trained_frequencies else None
    if vocabulary is None:
        return

    decoded_secret = decode(encoded_secret, vocabulary, "</s>") if encoded_secret else None
    if decoded_secret is None:
        return
    print("Decoded secret:", decoded_secret)

    translation_vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if translation_vocab is None:
        return
    print("Loaded vocab size:", len(translation_vocab))

    encoded = encode(
        text_to_translate,
        translation_vocab,
        "\u2581",
        None,
        "<unk>",
    )
    if encoded is None:
        return

    compare_len = min(20, len(encoded), len(reference))
    is_match = all(encoded[i] == reference[i] for i in range(compare_len))
    print("Encode matches reference:", is_match)


if __name__ == "__main__":
    main()
