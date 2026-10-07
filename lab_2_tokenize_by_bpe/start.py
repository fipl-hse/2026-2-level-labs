"""
BPE Tokenizer starter
"""

import json

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

    word_frequencies = collect_frequencies(text, start_of_word=None, end_of_word="</s>")
    if word_frequencies is None:
        print("Error: Failed to collect word frequencies.")
        return
    trained_frequencies = train(word_frequencies, num_merges=100)
    if trained_frequencies is None:
        print("Error: Failed to train tokenizer.")
        return
    print("Trained word frequencies (first 10):")
    for i, (word, freq) in enumerate(trained_frequencies.items()):
        if i >= 10:
            break
        print(f"  {word}: {freq}")
    vocabulary = get_vocabulary(trained_frequencies, unknown_token="<unk>")
    if vocabulary is None:
        print("Error: Failed to build vocabulary.")
        return
    print("\nVocabulary (first 20):")
    for i, (token, identifier) in enumerate(vocabulary.items()):
        if i >= 20:
            break
        print(f"  {repr(token)}: {identifier}")

    secret_vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocabulary.json")
    if secret_vocab is None:
        print("Error: Failed to load vocabulary.")
        return

    with open(
        "lab_2_tokenize_by_bpe/assets/encoded_text.json", "r", encoding="utf-8"
    ) as encoded_file:
        loaded_dict = json.load(encoded_file)
        encoded_ideal = loaded_dict["ideal_encoded_text"]

    decoded_secret = decode(encoded_ideal, secret_vocab, "</s>")
    if decoded_secret is None:
        print("Error: Failed to decode secret text.")
        return
    print("\nDecoded secret text:")
    print(decoded_secret)

    model_vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if model_vocab is None:
        print("Error: Failed to load model vocabulary.")
        return

    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as ru_file:
        ru_text = ru_file.read()

    encoded_ru = encode(ru_text, model_vocab, "\u2581", None, "<unk>")
    if encoded_ru is None:
        print("Error: Failed to encode Russian text.")
        return
    print("\nEncoded Russian text (first 10):")
    print(encoded_ru[:10])

    result = encoded_ru
    assert result, "Encoding not working"


if __name__ == "__main__":
    main()
