"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    decode,
    get_vocabulary,
    train,
)


def main() -> None:
    """
    Launches an implementation.
    """
    with open(
        "lab_2_tokenize_by_bpe/assets/text.txt",
        "r",
        encoding="utf-8",
    ) as text_file:
        text = text_file.read()

    word_frequencies = collect_frequencies(text, None, "</s>")
    assert word_frequencies is not None

    trained_frequencies = train(word_frequencies, 100)
    assert trained_frequencies is not None

    vocabulary = get_vocabulary(trained_frequencies, "<unk>")
    assert vocabulary is not None

    with open(
        "lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt",
        "r",
        encoding="utf-8",
    ) as secret_file:
        encoded_text = [int(token) for token in secret_file.read().split()]

    decoded_text = decode(encoded_text, vocabulary, "</s>")
    assert decoded_text is not None

    print("Decoded secret:", decoded_text)

    result = decoded_text
    assert result, "Decoding not working"


if __name__ == "__main__":
    main()
