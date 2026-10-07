"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
import os

from lab_2_tokenize_by_bpe.main import (
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
    word_frequencies = collect_frequencies(text, None, "</s>")
    print("Word frequencies:", word_frequencies)

    trained_frequencies = train(word_frequencies, 100)
    print("Trained frequencies:", trained_frequencies)

    if trained_frequencies is None:
        return

    vocabulary = get_vocabulary(trained_frequencies, "<unk>")
    if vocabulary is None:
        return

    secrets_folder = "lab_2_tokenize_by_bpe/assets/secrets"
    secret_files = sorted(os.listdir(secrets_folder))

    if not secret_files:
        return

    secret_path = os.path.join(secrets_folder, secret_files[0])
    with open(secret_path, "r", encoding="utf-8") as secret_file:
        raw_content = secret_file.read()

    encoded_text = [int(value) for value in raw_content.split()]

    decoded = decode(encoded_text, vocabulary, "</s>")
    print("Decoded secret:", decoded)


if __name__ == "__main__":
    main()
